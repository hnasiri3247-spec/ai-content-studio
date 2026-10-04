package com.aicontentstudio.presentation.viewmodel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aicontentstudio.domain.usecase.ImageGenerationService
import com.aicontentstudio.util.Resource
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ImageViewModel @Inject constructor(private val imageGenerationService: ImageGenerationService) : ViewModel() {
    private val _uiState = MutableStateFlow<ImageUiState>(ImageUiState.Idle)
    val uiState: StateFlow<ImageUiState> = _uiState.asStateFlow()

    fun generateImage(prompt: String, service: String) {
        if (prompt.isBlank()) { _uiState.value = ImageUiState.Error("پرامپت نمی‌تواند خالی باشد"); return }
        viewModelScope.launch {
            _uiState.value = ImageUiState.Loading
            imageGenerationService(prompt, service).collect { resource ->
                when (resource) {
                    is Resource.Success -> _uiState.value = ImageUiState.Success(resource.data ?: "")
                    is Resource.Error -> _uiState.value = ImageUiState.Error(resource.message ?: "خطا")
                    is Resource.Loading -> _uiState.value = ImageUiState.Loading
                }
            }
        }
    }
    sealed class ImageUiState { object Idle : ImageUiState(); object Loading : ImageUiState(); data class Success(val imageUrl: String) : ImageUiState(); data class Error(val message: String) : ImageUiState() }
}
