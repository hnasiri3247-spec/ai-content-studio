import os
base = "AIContentStudio"
dirs = ["app/src/main/java/com/aicontentstudio/data/local", "app/src/main/java/com/aicontentstudio/data/remote", "app/src/main/java/com/aicontentstudio/data/repository", "app/src/main/java/com/aicontentstudio/data/security", "app/src/main/java/com/aicontentstudio/domain/model", "app/src/main/java/com/aicontentstudio/domain/usecase", "app/src/main/java/com/aicontentstudio/presentation/ui", "app/src/main/java/com/aicontentstudio/presentation/viewmodel", "app/src/main/java/com/aicontentstudio/util"]
for d in dirs: os.makedirs(f"{base}/{d}", exist_ok=True)

files = {
"app/src/main/java/com/aicontentstudio/data/local/ChatMessageEntity.kt": """package com.aicontentstudio.data.local
import androidx.room.Entity
import androidx.room.PrimaryKey
@Entity(tableName = "chat_messages")
data class ChatMessageEntity(@PrimaryKey(autoGenerate = true) val id: Int = 0, val content: String, val isUser: Boolean, val timestamp: Long = System.currentTimeMillis(), val sessionId: String = "default")""",

"app/src/main/java/com/aicontentstudio/data/local/ChatDao.kt": """package com.aicontentstudio.data.local
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
@Dao
interface ChatDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertMessage(message: ChatMessageEntity)
    @Query("SELECT * FROM chat_messages WHERE sessionId = :sessionId ORDER BY timestamp ASC") fun getMessagesBySession(sessionId: String): Flow<List<ChatMessageEntity>>
}""",

"app/src/main/java/com/aicontentstudio/data/local/GeneratedContentEntity.kt": """package com.aicontentstudio.data.local
import androidx.room.Entity
import androidx.room.PrimaryKey
@Entity(tableName = "generated_content")
data class GeneratedContentEntity(@PrimaryKey(autoGenerate = true) val id: Int = 0, val prompt: String, val resultUrl: String?, val contentType: String, val serviceName: String, val timestamp: Long = System.currentTimeMillis())""",

"app/src/main/java/com/aicontentstudio/data/local/GeneratedContentDao.kt": """package com.aicontentstudio.data.local
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
@Dao
interface GeneratedContentDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertContent(content: GeneratedContentEntity)
    @Query("SELECT * FROM generated_content ORDER BY timestamp DESC") fun getAllContent(): Flow<List<GeneratedContentEntity>>
}""",

"app/src/main/java/com/aicontentstudio/data/remote/QwenApi.kt": """package com.aicontentstudio.data.remote
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
data class ChatRequest(val model: String, val messages: List<MessageDto>, val stream: Boolean = false)
data class MessageDto(val role: String, val content: String)
data class ChatResponse(val choices: List<ChoiceDto>)
data class ChoiceDto(val message: MessageDto)
interface QwenApi {
    @POST("v1/chat/completions") suspend fun getChatResponse(@Body request: ChatRequest): Response<ChatResponse>
}""",

"app/src/main/java/com/aicontentstudio/data/remote/ImageApi.kt": """package com.aicontentstudio.data.remote
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST
data class SubNPRequest(val prompt: String, val negative_prompt: String = "")
data class SubNPResponse(val status: String, val image_url: String?)
data class PixazoRequest(val prompt: String, val model: String = "flux-schnell")
data class PixazoResponse(val success: Boolean, val data: List<PixazoImageData>)
data class PixazoImageData(val url: String)
interface ImageApi {
    @POST("generate") suspend fun generateSubNP(@Body request: SubNPRequest): Response<SubNPResponse>
    @POST("v1/images/generations") suspend fun generatePixazo(@Body request: PixazoRequest): Response<PixazoResponse>
}""",

"app/src/main/java/com/aicontentstudio/data/repository/ChatRepository.kt": """package com.aicontentstudio.data.repository
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
}""",

"app/src/main/java/com/aicontentstudio/data/repository/ImageRepository.kt": """package com.aicontentstudio.data.repository
import com.aicontentstudio.data.local.GeneratedContentDao
import com.aicontentstudio.data.local.GeneratedContentEntity
import com.aicontentstudio.data.remote.*
import com.aicontentstudio.util.Resource
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

class ImageRepository @Inject constructor(private val imageApi: ImageApi, private val qwenApi: QwenApi, private val dao: GeneratedContentDao) {
    fun generateImage(prompt: String, service: String) = flow<Resource<String>> {
        emit(Resource.Loading())
        try {
            val translatedPrompt = translatePrompt(prompt)
            val imageUrl = when (service.uppercase()) {
                "SUBNP" -> callSubNP(translatedPrompt)
                "PIXAZO" -> callPixazo(translatedPrompt)
                else -> throw IllegalArgumentException("سرویس نامعتبر")
            }
            dao.insertContent(GeneratedContentEntity(prompt = prompt, resultUrl = imageUrl, contentType = "IMAGE", serviceName = service.uppercase()))
            emit(Resource.Success(imageUrl))
        } catch (e: Exception) {
            emit(Resource.Error(e.message ?: "خطا در تولید تصویر"))
        }
    }
    private suspend fun translatePrompt(faPrompt: String): String {
        return try {
            val request = ChatRequest(model = "qwen-turbo", messages = listOf(MessageDto("system", "Translate to English for AI image generator. Only return English text."), MessageDto("user", faPrompt)))
            val response = qwenApi.getChatResponse(request)
            response.body()?.choices?.firstOrNull()?.message?.content ?: faPrompt
        } catch (e: Exception) { faPrompt }
    }
    private suspend fun callSubNP(prompt: String): String {
        val response = imageApi.generateSubNP(SubNPRequest(prompt = prompt))
        if (response.isSuccessful && response.body()?.status == "success") return response.body()!!.image_url ?: throw Exception("URL یافت نشد")
        throw Exception("خطا در SubNP: ${response.code()}")
    }
    private suspend fun callPixazo(prompt: String): String {
        val response = imageApi.generatePixazo(PixazoRequest(prompt = prompt, model = "flux-schnell"))
        if (response.isSuccessful && response.body()?.success == true) return response.body()!!.data.firstOrNull()?.url ?: throw Exception("URL یافت نشد")
        throw Exception("خطا در Pixazo: ${response.code()}")
    }
}""",

"app/src/main/java/com/aicontentstudio/domain/usecase/ImageGenerationService.kt": """package com.aicontentstudio.domain.usecase
import com.aicontentstudio.data.repository.ImageRepository
import com.aicontentstudio.util.Resource
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

class ImageGenerationService @Inject constructor(private val repository: ImageRepository) {
    operator fun invoke(prompt: String, selectedService: String): Flow<Resource<String>> {
        if (prompt.isBlank()) return flow { emit(Resource.Error("پرامپت نمی‌تواند خالی باشد")) }
        return repository.generateImage(prompt, selectedService)
    }
}""",

"app/src/main/java/com/aicontentstudio/util/Resource.kt": """package com.aicontentstudio.util
sealed class Resource<T>(val data: T? = null, val message: String? = null) {
    class Success<T>(data: T) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
    class Loading<T>(data: T? = null) : Resource<T>(data)
}"""
}

for path, content in files.items():
    with open(f"{base}/{path}", "w", encoding="utf-8") as f:
        f.write(content)
print("✅ بخش اول کدها (Data و Domain) با موفقیت اضافه شد!")


