package com.aicontentstudio.presentation.viewmodel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aicontentstudio.data.local.ChatMessageEntity
import com.aicontentstudio.data.repository.ChatRepository
import com.aicontentstudio.util.Resource
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ChatViewModel @Inject constructor(private val repository: ChatRepository) : ViewModel() {
    private val _sessionId = "session_1"
    val messages: StateFlow<List<ChatMessageEntity>> = repository.getMessages(_sessionId).stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
    private val _uiState = MutableStateFlow<UiState>(UiState.Idle)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun sendMessage(text: String) {
        if (text.isBlank()) return
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.sendMessage(_sessionId, text).collect { resource ->
                when (resource) {
                    is Resource.Success -> _uiState.value = UiState.Idle
                    is Resource.Error -> _uiState.value = UiState.Error(resource.message ?: "خطا")
                    is Resource.Loading -> _uiState.value = UiState.Loading
                }
            }
        }
    }
    sealed class UiState { object Idle : UiState(); object Loading : UiState(); data class Error(val message: String) : UiState() }
}
