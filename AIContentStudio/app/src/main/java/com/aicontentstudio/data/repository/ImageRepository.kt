package com.aicontentstudio.data.repository
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
}