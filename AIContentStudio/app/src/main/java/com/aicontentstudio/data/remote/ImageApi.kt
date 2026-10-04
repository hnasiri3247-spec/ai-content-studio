package com.aicontentstudio.data.remote
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
}