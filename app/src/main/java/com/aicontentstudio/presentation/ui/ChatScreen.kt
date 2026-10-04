package com.aicontentstudio.presentation.ui
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.aicontentstudio.presentation.viewmodel.ChatViewModel

@Composable
fun ChatScreen(viewModel: ChatViewModel = hiltViewModel()) {
    val messages by viewModel.messages.collectAsState()
    val uiState by viewModel.uiState.collectAsState()
    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    LaunchedEffect(messages.size) { if (messages.isNotEmpty()) listState.animateScrollToItem(messages.size - 1) }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        LazyColumn(state = listState, modifier = Modifier.weight(1f).fillMaxWidth(), contentPadding = PaddingValues(vertical = 8.dp)) {
            items(messages) { message ->
                Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = if (message.isUser) Arrangement.End else Arrangement.Start) {
                    Surface(color = if (message.isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant, shape = MaterialTheme.shapes.medium, modifier = Modifier.widthIn(max = 280.dp).padding(horizontal = 8.dp)) {
                        Text(text = message.content, modifier = Modifier.padding(12.dp), color = if (message.isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
            if (uiState is ChatViewModel.UiState.Loading) {
                item { Row(modifier = Modifier.fillMaxWidth().padding(8.dp)) { CircularProgressIndicator(modifier = Modifier.size(24.dp)); Spacer(modifier = Modifier.width(8.dp)); Text("در حال نوشتن...") } }
            }
        }
        if (uiState is ChatViewModel.UiState.Error) { Text(text = (uiState as ChatViewModel.UiState.Error).message, color = MaterialTheme.colorScheme.error, modifier = Modifier.fillMaxWidth().padding(8.dp)) }
        Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), verticalAlignment = Alignment.Bottom) {
            OutlinedTextField(value = inputText, onValueChange = { inputText = it }, modifier = Modifier.weight(1f), placeholder = { Text("پیام خود را بنویسید...") }, maxLines = 4)
            Spacer(modifier = Modifier.width(8.dp))
            Button(onClick = { if (inputText.isNotBlank()) { viewModel.sendMessage(inputText); inputText = "" } }, enabled = uiState !is ChatViewModel.UiState.Loading, modifier = Modifier.height(56.dp)) { Text("ارسال") }
        }
    }
}
