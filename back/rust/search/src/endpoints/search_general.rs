use crate::{
    endpoints::{
        recipe::TOP, EndpointResponse, ErrorResponse, InputPayload, SearchResponse,
        INTERNAL_SERVER_ERROR,
    },
    get_context,
    repository::{
        get_repository,
        models::recipe::Recipe,
        service::{
            allergen::Repository as AllergenRepository, recipe::Repository as RecipeRepository,
            tag::Repository as TagRepository, user::Repository as UserRepository,
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

#[endpoint]
pub async fn search_general(
    payload: JsonBody<InputPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<Recipe>> {
    let context = get_context!(res);

    let payload = payload.into_inner();
    let data = payload.data.clone();

    let recipes = match context.recipe_collection.search(payload).await {
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

            value
        }
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    let users = match context.user_collection.find_by_name(data).await {
        Ok(value) => value,
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            return Json(EndpointResponse::Error(ErrorResponse {
                message: e.to_string(),
            }));
        }
    };

    Json(EndpointResponse::SuccessSearch(SearchResponse {
        recipes,
        users,
    }))
}
