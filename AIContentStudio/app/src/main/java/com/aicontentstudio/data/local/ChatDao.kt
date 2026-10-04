package com.aicontentstudio.data.local
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
@Dao
interface ChatDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertMessage(message: ChatMessageEntity)
    @Query("SELECT * FROM chat_messages WHERE sessionId = :sessionId ORDER BY timestamp ASC") fun getMessagesBySession(sessionId: String): Flow<List<ChatMessageEntity>>
}