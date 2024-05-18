use crate::{
    get_redirect_url,
    models::{
        rating::RatingList,
        ErrorResponse
    },
    config::get_global_context,
    endpoints::{
        redirect,
        rating::{SERVICE, EndpointResponse}
    }
};
use salvo::{
    Writer,
    oapi::endpoint,
    http::StatusCode,
    prelude::Json,
    Request, Response
};
use anyhow::Result;
use reqwest::{Client, Method};
use salvo::oapi::extract::QueryParam;
use tracing::error;
use tracing::log::debug;

async fn get_rating_response(
    method: Method,
    service_url: &str,
    parent_id: String,
    params: &[(&str, u32)],
) -> Result<EndpointResponse> {
    let response = Client::new()
        .request(method, service_url)
        .query(&[("parent_id", parent_id)])
        .query(params)
        .send()
        .await?;

    debug!("{:#?}", response.url().as_str());

    if response.status().is_success() {
        Ok(EndpointResponse::RatingList(response.json::<RatingList>().await?))
    } else {
        Ok(EndpointResponse::Error(
            response.json::<ErrorResponse>().await?,
        ))
    }
}

#[endpoint(
    parameters(
        ("parent_id" = String, description = "Rating id"),
        ("start" = i64, description = "Start value"),
        ("count" = i64, description = "Count value")
    )
)]
pub async fn get_rating_endpoint(req: &mut Request, res: &mut Response, start: QueryParam<u32, true>, count: QueryParam<u32, true>) -> Json<EndpointResponse> {
    let url: String = get_redirect_url!(req, res, SERVICE);
    println!("test: {:#?}, {}, {}", req.queries(), start, count);
    let parent_id= req.param::<String>("parent_id").unwrap_or_default();

    return match get_rating_response(
        Method::GET,
        url.as_str(),
        parent_id,
        &[("start", start.into_inner()), ("count", count.into_inner())],
    )
    .await
    {
        Ok(response) => Json(response),
        Err(_) => {
            res.status_code(StatusCode::BAD_REQUEST);
            Json(EndpointResponse::Error(ErrorResponse::default()))
        }
    };
}
