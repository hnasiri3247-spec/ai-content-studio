package com.aicontentstudio.data.remote
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
data class ChatRequest(val model: String, val messages: List<MessageDto>, val stream: Boolean = false)
data class MessageDto(val role: String, val content: String)
data class ChatResponse(val choices: List<ChoiceDto>)
data class ChoiceDto(val message: MessageDto)
interface QwenApi {
    @POST("v1/chat/completions") suspend fun getChatResponse(@Body request: ChatRequest): Response<ChatResponse>
}