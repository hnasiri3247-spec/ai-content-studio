package com.aicontentstudio.domain.usecase
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
}