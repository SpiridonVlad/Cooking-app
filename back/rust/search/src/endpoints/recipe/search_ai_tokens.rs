use crate::{
    endpoints::{
        recipe::{AiTokensPayload, TOP},
        AggregationResponse, EndpointResponse, ErrorResponse, INTERNAL_SERVER_ERROR,
    },
    get_context,
    repository::{
        get_repository,
        models::recipe::Recipe,
        service::{
            allergen::Repository as AllergenRepository, recipe::Repository as RecipeRepository,
            tag::Repository as TagRepository,
        },
    },
};
use salvo::{
    http::StatusCode,
    oapi::extract::JsonBody,
    prelude::{endpoint, Json, Writer},
    Response,
};
use tracing::error;

#[endpoint(
    responses(
        (
            status_code = StatusCode::OK,
            body = AggregationResponse<Recipe>,
            example = json!(AggregationResponse::<Recipe>::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        )
    )
)]
pub async fn search_ai_tokens(
    ai_tokens: JsonBody<AiTokensPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_context!(res);

    return match context
        .recipe_collection
        .find_by_tokens(&ai_tokens.tokens)
        .await
    {
        Ok(mut value) => {
            if value.data.is_empty() {
                return Json(EndpointResponse::default());
            }

            for recipe in value.data.iter_mut() {
                let top_tags = match context
                    .tag_collection
                    .filter_top_x_tags(recipe.tags.clone(), TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(EndpointResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.tags = top;
                }
                let top_tags = match context
                    .allergen_collection
                    .filter_top_x_allergens(recipe.allergens.clone(), TOP)
                    .await
                {
                    Ok(value) => value,
                    Err(_) => {
                        res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
                        return Json(EndpointResponse::Error(ErrorResponse {
                            message: INTERNAL_SERVER_ERROR.to_string(),
                        }));
                    }
                };
                if let Some(top) = top_tags {
                    recipe.allergens = top;
                }
            }
            Json(EndpointResponse::Success(value))
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }))
        }
    };
}
