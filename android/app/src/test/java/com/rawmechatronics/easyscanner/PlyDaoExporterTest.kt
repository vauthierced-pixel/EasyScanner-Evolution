package com.rawmechatronics.easyscanner

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import java.io.IOException
import java.io.StringWriter
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.file.Files

class PlyDaoExporterTest {
    private fun fileFor(points: List<FloatArray>): File {
        val h = ("ply\nformat binary_little_endian 1.0\n" +
            "element vertex " + points.size + "\n" +
            "property float x\nproperty float y\nproperty float z\n" +
            "property uchar red\nproperty uchar green\nproperty uchar blue\n" +
            "end_header\n").toByteArray(Charsets.US_ASCII)
        val b = ByteBuffer.allocate(points.size * 15).order(ByteOrder.LITTLE_ENDIAN)
        for (p in points) {
            for (v in p) b.putFloat(v)
            b.put(1); b.put(2); b.put(3)
        }
        val result = Files.createTempFile("dao-export-test", ".ply").toFile()
        result.writeBytes(h + b.array())
        return result
    }

    @Test
    fun xyzExportsAllValidPointsAndPreservesOriginal() {
        val file = fileFor(listOf(floatArrayOf(1.125f, -2.5f, 3f), floatArrayOf(4f, 5f, 6f)))
        try {
            val before = file.readBytes()
            val output = StringWriter()
            val stats = PlyDaoExporter.convert(file, output, PlyDaoExporter.Format.XYZ)
            assertEquals("1.125 -2.5 3\n4 5 6\n", output.toString())
            assertEquals(2, stats.inputPoints)
            assertEquals(2, stats.outputPoints)
            assertTrue(before.contentEquals(file.readBytes()))
        } finally { file.delete() }
    }

    @Test
    fun csvHasMetricHeaderAndRemovesInvalidCoordinates() {
        val file = fileFor(listOf(floatArrayOf(1f, 2f, 3f), floatArrayOf(Float.NaN, 0f, 0f)))
        try {
            val output = StringWriter()
            val stats = PlyDaoExporter.convert(file, output, PlyDaoExporter.Format.CSV)
            assertEquals("X_mm;Y_mm;Z_mm\n1;2;3\n", output.toString())
            assertEquals(1, stats.invalidPoints)
            assertEquals(1, stats.outputPoints)
        } finally { file.delete() }
    }

    @Test
    fun voxelReductionHandlesNegativeCoordinatesAndRepeatedCells() {
        val file = fileFor(listOf(
            floatArrayOf(-0.2f, 0.1f, 0f),
            floatArrayOf(-0.7f, 0.8f, 0.4f),
            floatArrayOf(0.1f, 0.2f, 0f)
        ))
        try {
            val output = StringWriter()
            val stats = PlyDaoExporter.convert(file, output, PlyDaoExporter.Format.XYZ, 1.0)
            assertEquals(2, stats.outputPoints)
            assertEquals(1, stats.repeatedCells)
            assertEquals(2, output.toString().trim().lines().size)
        } finally { file.delete() }
    }

    @Test(expected = IOException::class)
    fun rejectsTruncatedPly() {
        val file = fileFor(listOf(floatArrayOf(1f, 2f, 3f)))
        try {
            file.writeBytes(file.readBytes().dropLast(5).toByteArray())
            PlyDaoExporter.convert(file, StringWriter(), PlyDaoExporter.Format.XYZ)
        } finally { file.delete() }
    }

    @Test
    fun supportsReorderedDoubleCoordinates() {
        val header = ("ply\nformat binary_little_endian 1.0\n" +
            "element vertex 1\nproperty double z\nproperty double x\nproperty double y\nend_header\n")
            .toByteArray(Charsets.US_ASCII)
        val body = ByteBuffer.allocate(24).order(ByteOrder.LITTLE_ENDIAN)
            .putDouble(3.25).putDouble(1.5).putDouble(-2.0).array()
        val file = Files.createTempFile("dao-reorder", ".ply").toFile()
        try {
            file.writeBytes(header + body)
            val output = StringWriter()
            PlyDaoExporter.convert(file, output, PlyDaoExporter.Format.XYZ)
            assertEquals("1.5 -2 3.25\n", output.toString())
        } finally { file.delete() }
    }
}
