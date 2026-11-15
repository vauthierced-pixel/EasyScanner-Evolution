package com.rawmechatronics.easyscanner

import java.io.File
import java.io.IOException
import java.io.RandomAccessFile
import java.io.Writer
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale
import kotlin.math.floor

/**
 * Converts a binary little-endian PLY to metric XYZ/CSV for desktop CAD.
 *
 * Reads every vertex directly from disk, without the display-only 1.5M point
 * thinning done by PlyCloud. The source PLY is never modified.
 *
 * Optional 1 mm voxel filtering only removes coincident / near-coincident
 * points (one point per cubic cell); it is NOT a statistical outlier filter.
 */
object PlyDaoExporter {
    enum class Format(val extension: String) { XYZ("xyz"), CSV("csv") }
    data class Result(val inputPoints: Int, val outputPoints: Int, val invalidPoints: Int, val repeatedCells: Int)

    private data class Property(val name: String, val type: String, val offset: Int)
    private data class Cell(val x: Long, val y: Long, val z: Long)

    private const val MAX_HEADER_BYTES = 65536
    private const val MAX_VOXEL_CELLS = 600_000
    private val sizes = mapOf(
        "char" to 1, "uchar" to 1, "int8" to 1, "uint8" to 1,
        "short" to 2, "ushort" to 2, "int16" to 2, "uint16" to 2,
        "int" to 4, "uint" to 4, "int32" to 4, "uint32" to 4,
        "float" to 4, "float32" to 4, "double" to 8, "float64" to 8
    )

    fun convert(source: File, output: Writer, format: Format, voxelMm: Double? = null): Result {
        require(voxelMm == null || voxelMm.isFinite() && voxelMm > 0.0)
        RandomAccessFile(source, "r").use { input ->
            if (input.readLine() != "ply") throw IOException("Not a PLY file")
            var firstElement: String? = null
            var vertexCount = -1
            var vertexSection = false
            var stride = 0
            val properties = ArrayList<Property>()
            var binary = false
            var ended = false
            while (input.filePointer <= MAX_HEADER_BYTES) {
                val line = input.readLine() ?: break
                val words = line.trim().split(Regex("\\s+"))
                when (words.firstOrNull()) {
                    "format" -> binary = words.getOrNull(1) == "binary_little_endian"
                    "element" -> {
                        if (words.size < 3) throw IOException("Malformed element header")
                        if (firstElement == null) firstElement = words[1]
                        vertexSection = words[1] == "vertex"
                        if (vertexSection) vertexCount = words[2].toIntOrNull() ?: -1
                    }
                    "property" -> if (vertexSection) {
                        if (words.size != 3 || words[1] == "list") throw IOException("Unsupported vertex property")
                        val size = sizes[words[1]] ?: throw IOException("Unsupported PLY type: " + words[1])
                        properties.add(Property(words[2], words[1], stride))
                        stride += size
                    }
                    "end_header" -> { ended = true; break }
                }
            }
            if (!ended || !binary || firstElement != "vertex" || vertexCount < 0 || stride <= 0) {
                throw IOException("Expected binary little-endian PLY with vertices first")
            }
            fun find(name: String): Property =
                properties.firstOrNull { it.name == name } ?: throw IOException("Missing PLY property: " + name)
            val px = find("x")
            val py = find("y")
            val pz = find("z")
            if (vertexCount.toLong() * stride > input.length() - input.filePointer) {
                throw IOException("Truncated PLY vertex data")
            }

            val cellSet = if (voxelMm != null) HashSet<Cell>() else null
            val record = ByteArray(stride)
            val buffer = ByteBuffer.wrap(record).order(ByteOrder.LITTLE_ENDIAN)
            val decimal = DecimalFormat("0.###", DecimalFormatSymbols(Locale.US)).apply {
                isGroupingUsed = false
            }

            if (format == Format.CSV) output.write("X_mm;Y_mm;Z_mm\n")
            var invalid = 0
            var repeated = 0
            var accepted = 0
            repeat(vertexCount) {
                input.readFully(record)
                val x = value(buffer, px)
                val y = value(buffer, py)
                val z = value(buffer, pz)
                if (!x.isFinite() || !y.isFinite() || !z.isFinite()) {
                    invalid++
                } else {
                    val cell = if (voxelMm != null) Cell(
                        floor(x / voxelMm).toLong(),
                        floor(y / voxelMm).toLong(),
                        floor(z / voxelMm).toLong()
                    ) else null
                    if (cell != null && !cellSet!!.add(cell)) {
                        repeated++
                    } else {
                        if (cellSet != null && cellSet.size > MAX_VOXEL_CELLS) {
                            throw IOException("Too many voxels for safe on-phone filtering; use the full export")
                        }
                        val separator = if (format == Format.CSV) ";" else " "
                        output.write(decimal.format(x))
                        output.write(separator)
                        output.write(decimal.format(y))
                        output.write(separator)
                        output.write(decimal.format(z))
                        output.write("\n")
                        accepted++
                    }
                }
            }
            output.flush()
            return Result(vertexCount, accepted, invalid, repeated)
        }
    }

    private fun value(b: ByteBuffer, p: Property): Double {
        val at = p.offset
        return when (p.type) {
            "float", "float32" -> b.getFloat(at).toDouble()
            "double", "float64" -> b.getDouble(at)
            "char", "int8" -> b.get(at).toDouble()
            "uchar", "uint8" -> (b.get(at).toInt() and 255).toDouble()
            "short", "int16" -> b.getShort(at).toDouble()
            "ushort", "uint16" -> (b.getShort(at).toInt() and 65535).toDouble()
            "int", "int32" -> b.getInt(at).toDouble()
            "uint", "uint32" -> (b.getInt(at).toLong() and 0xFFFFFFFFL).toDouble()
            else -> throw IOException("Unsupported PLY type: " + p.type)
        }
    }
}
