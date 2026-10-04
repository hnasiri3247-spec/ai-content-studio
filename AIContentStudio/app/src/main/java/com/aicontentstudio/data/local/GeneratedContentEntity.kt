package com.aicontentstudio.data.local
import androidx.room.Entity
import androidx.room.PrimaryKey
@Entity(tableName = "generated_content")
data class GeneratedContentEntity(@PrimaryKey(autoGenerate = true) val id: Int = 0, val prompt: String, val resultUrl: String?, val contentType: String, val serviceName: String, val timestamp: Long = System.currentTimeMillis())