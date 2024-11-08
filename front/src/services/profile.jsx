import axios from 'axios'
import { authHeader } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

export const getProfile = async (profileId, token) => {
    const response = await axios.get(`${API_URL}/users/${profileId}`, {
        headers: { ...authHeader(token) },
    })
    return response.data
}

export const getFullProfile = async (id, token) => {
    return (
        await axios.get(`${API_URL}/users/${id}/profile`, {
            headers: { Authorization: token },
        })
    ).data
}

export const updateProfile = async (id, token, data) => {
    await axios.patch(`${API_URL}/users/${id}`, data, {
        headers: { Authorization: token },
    })
}

export const getFollowers = async (profileId, start, count) => {
    const response = await axios.get(`${API_URL}/users/${profileId}/followers`, {
        headers: {},
        params: { start: start, count: count },
    })
    return response.data
}
export const getFollowing = async (profileId, start, count) => {
    const response = await axios.get(`${API_URL}/users/${profileId}/following`, {
        params: { start: start, count: count },
    })
    return response.data
}

export const follow = async (userId, otherUserId, token) => {
    await axios.post(
        `${API_URL}/users/${userId}/follow`,
        { followsId: otherUserId },
        {
            headers: { Authorization: token },
        }
    )
}

export const unfollow = async (userId, otherUserId, token) => {
    await axios.delete(`${API_URL}/users/${userId}/follow`, {
        headers: { Authorization: token },
        data: { followsId: otherUserId },
    })
}

export const getSavedRecipes = async (profileId, start, count, token) => {
    const response = await axios.get(`${API_URL}/users/${profileId}/saved-recipes`, {
        headers: { ...authHeader(token) },
        params: { start, count },
    })
    console.log(response)
    return response.data
}
