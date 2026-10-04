package com.aicontentstudio.data.local
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
@Dao
interface GeneratedContentDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE) suspend fun insertContent(content: GeneratedContentEntity)
    @Query("SELECT * FROM generated_content ORDER BY timestamp DESC") fun getAllContent(): Flow<List<GeneratedContentEntity>>
}