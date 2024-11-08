use crate::{
    context::get_global_context,
    endpoints::{EndpointResponse, ErrorCodes, ErrorResponse},
    get_endpoint_context,
    repository::{models::user::User, service::user::Repository as UserRepository},
};
use salvo::{
    Writer,
    http::StatusCode,
    oapi::extract::JsonBody,
    prelude::{endpoint, Json},
    Response,
};
use tracing::error;

use super::SearchUsersPayload;

#[endpoint]
pub async fn search_users(
    payload: JsonBody<SearchUsersPayload>,
    res: &mut Response,
) -> Json<EndpointResponse<User>> {
    let context = get_endpoint_context!(res);

    match context
        .repository
        .user_collection
        .search(payload.into_inner().into_params())
        .await
    {
        Ok(value) => Json(EndpointResponse::Success(value)),
        Err(e) => {
            error!("Error: {e}");
            res.status_code(StatusCode::INTERNAL_SERVER_ERROR);
            Json(EndpointResponse::Error(ErrorResponse {
                error_code: ErrorCodes::DbError as u32,
            }))
        }
    }
}
