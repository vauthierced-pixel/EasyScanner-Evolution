package com.rawmechatronics.easyscanner

import android.content.ContentValues
import android.content.Context
import android.os.Environment
import android.provider.MediaStore
import java.io.File
import java.io.IOException
import java.util.Locale

/**
 * Writes additional, non-destructive CAD exports to public Downloads.
 * No storage permission is needed for new MediaStore entries on Android 10+.
 */
object DaoDownloads {
    fun export(
        context: Context,
        source: File,
        format: PlyDaoExporter.Format,
        voxelMm: Double?
    ): PlyDaoExporter.Result {
        val stem = source.nameWithoutExtension
            .replace(Regex("[^A-Za-z0-9_-]"), "_")
            .take(60)
            .ifEmpty { "scan" }
        val suffix = if (voxelMm != null) "_grid1mm" else "_full"
        val filename = stem + suffix + "." + format.extension
        val resolver = context.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.Downloads.DISPLAY_NAME, filename)
            put(MediaStore.Downloads.MIME_TYPE, if (format == PlyDaoExporter.Format.CSV) "text/csv" else "text/plain")
            put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/EasyScanner/DAO/")
            put(MediaStore.Downloads.IS_PENDING, 1)
        }
        val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
            ?: throw IOException("Cannot create the output in Downloads")
        try {
            val stream = resolver.openOutputStream(uri) ?: throw IOException("Cannot open output")
            val result = stream.bufferedWriter(Charsets.UTF_8).use { out ->
                PlyDaoExporter.convert(source, out, format, voxelMm)
            }
            resolver.update(uri, ContentValues().apply {
                put(MediaStore.Downloads.IS_PENDING, 0)
            }, null, null)
            return result
        } catch (error: Exception) {
            runCatching { resolver.delete(uri, null, null) }
            throw error
        }
    }
}
