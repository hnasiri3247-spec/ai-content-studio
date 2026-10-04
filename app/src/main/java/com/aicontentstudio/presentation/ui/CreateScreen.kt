package com.aicontentstudio.presentation.ui
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import coil.compose.AsyncImage
import com.aicontentstudio.presentation.viewmodel.ImageViewModel

@Composable
fun CreateScreen(viewModel: ImageViewModel = hiltViewModel()) {
    var prompt by remember { mutableStateOf("") }
    var selectedService by remember { mutableStateOf("SubNP") }
    val uiState by viewModel.uiState.collectAsState()
    val services = listOf("SubNP", "Pixazo")

    Column(modifier = Modifier.fillMaxSize().padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Text("تولید تصویر با هوش مصنوعی", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = prompt, onValueChange = { prompt = it }, label = { Text("توصیف تصویر") }, modifier = Modifier.fillMaxWidth(), minLines = 3)
        Spacer(modifier = Modifier.height(16.dp))
        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text("سرویس: ")
            Spacer(modifier = Modifier.width(8.dp))
            var expanded by remember { mutableStateOf(false) }
            ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                OutlinedTextField(value = selectedService, onValueChange = {}, readOnly = true, trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) }, modifier = Modifier.menuAnchor())
                ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                    services.forEach { service -> DropdownMenuItem(text = { Text(service) }, onClick = { selectedService = service; expanded = false }) }
                }
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
        Button(onClick = { viewModel.generateImage(prompt, selectedService) }, enabled = uiState !is ImageViewModel.ImageUiState.Loading, modifier = Modifier.fillMaxWidth().height(50.dp)) {
            if (uiState is ImageViewModel.ImageUiState.Loading) { CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary); Spacer(modifier = Modifier.width(8.dp)) }
            Text("تولید تصویر")
        }
        Spacer(modifier = Modifier.height(24.dp))
        if (uiState is ImageViewModel.ImageUiState.Error) { Text(text = (uiState as ImageViewModel.ImageUiState.Error).message, color = MaterialTheme.colorScheme.error) }
        if (uiState is ImageViewModel.ImageUiState.Success) {
            val url = (uiState as ImageViewModel.ImageUiState.Success).imageUrl
            Card(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) { AsyncImage(model = url, contentDescription = "Generated Image", modifier = Modifier.fillMaxSize()) }
        }
    }
}
