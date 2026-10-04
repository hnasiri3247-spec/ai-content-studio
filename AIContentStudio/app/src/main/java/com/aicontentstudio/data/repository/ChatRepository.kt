package com.aicontentstudio.data.repository
import com.aicontentstudio.data.local.ChatDao
import com.aicontentstudio.data.local.ChatMessageEntity
import com.aicontentstudio.data.remote.ChatRequest
import com.aicontentstudio.data.remote.MessageDto
import com.aicontentstudio.data.remote.QwenApi
import com.aicontentstudio.util.Resource
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

class ChatRepository @Inject constructor(private val api: QwenApi, private val dao: ChatDao) {
    fun getMessages(sessionId: String): Flow<List<ChatMessageEntity>> = dao.getMessagesBySession(sessionId)
    suspend fun sendMessage(sessionId: String, userMessage: String): Flow<Resource<String>> = flow {
        emit(Resource.Loading())
        try {
            dao.insertMessage(ChatMessageEntity(content = userMessage, isUser = true, sessionId = sessionId))
            val request = ChatRequest(model = "qwen-turbo", messages = listOf(MessageDto("user", userMessage)))
            val response = api.getChatResponse(request)
            if (response.isSuccessful && response.body() != null) {
                val aiText = response.body()!!.choices.firstOrNull()?.message?.content ?: "پاسخی دریافت نشد."
                dao.insertMessage(ChatMessageEntity(content = aiText, isUser = false, sessionId = sessionId))
                emit(Resource.Success(aiText))
            } else {
                emit(Resource.Error("خطا در ارتباط با سرور: ${response.code()}"))
            }
        } catch (e: Exception) {
            emit(Resource.Error(e.message ?: "خطای ناشناخته"))
        }
    }
}