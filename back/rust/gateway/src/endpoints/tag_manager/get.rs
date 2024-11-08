use crate::endpoints::tag_manager::SERVICE;
use crate::endpoints::{get_response, EndpointResponse, FAILED_RESPONSE, SUCCESSFUL_RESPONSE};
use crate::models::tags::Tags;
use crate::models::ErrorResponse;
use reqwest::{Method, StatusCode};
use salvo::oapi::endpoint;
use salvo::oapi::extract::QueryParam;
use salvo::prelude::Json;
use salvo::{Request, Response, Writer};
use tracing::error;

#[endpoint(
    responses
    (
        (
            status_code = StatusCode::OK,
            description = SUCCESSFUL_RESPONSE,
            body = Tags,
            example = json!(Tags::default())
        ),
        (
            status_code = StatusCode::INTERNAL_SERVER_ERROR,
            description = FAILED_RESPONSE,
            body = ErrorResponse,
            example = json!(ErrorResponse::default())
        ),
    )
)]
pub async fn get_tags(
    req: &mut Request,
    res: &mut Response,
    starting_with: QueryParam<String, true>,
) -> Json<EndpointResponse<Tags>> {
    let uri = req.uri().path();
    let parts: Vec<&str> = uri.split('/').collect();
    let new_url = parts[3..].join("/");
    let url: String = format!("{SERVICE}/{new_url}");
    return match get_response::<[(&str, String); 1], &str, Tags>(
        Method::GET,
        url,
        Some(&[("starting_with", starting_with.into_inner())]),
        None,
        Some(req.headers().clone()),
        false,
    )
    .await {
        Ok(item) => {
            if let EndpointResponse::Error((error_code, status_code)) = item {
                res.status_code(StatusCode::from_u16(status_code).unwrap_or(StatusCode::INTERNAL_SERVER_ERROR));
                Json(EndpointResponse::ServerError(error_code))
            } else {
                Json(item)
            }
        },
        Err(e) => {
            error!("{e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::default())
        }
    }
}
