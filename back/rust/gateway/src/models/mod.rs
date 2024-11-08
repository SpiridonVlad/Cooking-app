use salvo::http::StatusCode;
use salvo::oapi::ToSchema;
use serde::{Deserialize, Serialize};

pub mod ai;
pub mod allergens;
pub mod credentials_change_requester;
pub mod email;
pub mod follow_manager;
pub mod hash;
pub mod image_storage;
pub mod login;
pub mod message_history;
pub mod password_changer;
pub mod patch_profile;
pub mod rating;
pub mod recipe;
pub mod register;
pub mod role_changer;
pub mod search;
pub mod search_history;
pub mod tags;
pub mod token_validator;
pub mod user;
pub mod username_changer;

#[derive(Serialize, Deserialize, ToSchema, Debug)]
#[serde(rename_all = "camelCase")]
pub struct ErrorResponse {
    pub error_code: u32,
}

impl Default for ErrorResponse {
    fn default() -> Self {
        Self {
            error_code: u32::from(StatusCode::INTERNAL_SERVER_ERROR.as_u16()),
        }
    }
}
