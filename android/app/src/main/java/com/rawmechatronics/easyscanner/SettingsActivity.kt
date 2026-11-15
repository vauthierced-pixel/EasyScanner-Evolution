package com.rawmechatronics.easyscanner

import android.graphics.ImageFormat
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.os.Bundle
import android.util.Size
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.preference.ListPreference
import androidx.preference.Preference
import androidx.preference.PreferenceFragmentCompat
import java.util.Locale

class SettingsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        padBelowBars(findViewById(android.R.id.content))
        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction().replace(android.R.id.content, Fragment()).commit()
        }
    }

    class Fragment : PreferenceFragmentCompat() {
        override fun onCreatePreferences(savedInstanceState: Bundle?, rootKey: String?) {
            setPreferencesFromResource(R.xml.preferences, rootKey)
            val mgr = requireContext().getSystemService(CameraManager::class.java)
            val fps = AppSettings.load(requireContext()).targetFps
            val cams = CameraInfo.backCameraIds(mgr).map { CameraInfo.query(mgr, it, fps, 0) }
            findPreference<ListPreference>("camera_id")?.apply {
                entries = cams.map { it.label }.toTypedArray()
                entryValues = cams.map { it.id }.toTypedArray()
                if (value == null && cams.isNotEmpty()) value = cams.first().id
            }
            findPreference<Preference>("camera_diagnostic")?.setOnPreferenceClickListener {
                val report = runCatching { cameraReport(mgr) }
                    .getOrElse { getString(R.string.camera_diag_error, it.message ?: it.javaClass.simpleName) }
                AlertDialog.Builder(requireContext())
                    .setTitle(R.string.camera_diag_title)
                    .setMessage(report)
                    .setPositiveButton(android.R.string.ok, null)
                    .show()
                true
            }
        }

        /**
         * Reports only capabilities exposed by Android Camera2.
         * A listed physical ID is not necessarily separately openable.
         * Measured analysis size and FPS are shown in the scanner HUD instead.
         */
        private fun cameraReport(mgr: CameraManager): String {
            val st = AppSettings.load(requireContext())
            val availableIds = CameraInfo.backCameraIds(mgr)
            val id = st.cameraId.takeIf { it in availableIds } ?: availableIds.firstOrNull()
                ?: return getString(R.string.no_camera)
            val c = mgr.getCameraCharacteristics(id)
            val info = CameraInfo.query(mgr, id, st.targetFps, st.maxLongSide)
            val map = c.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP)
            val yuvMax = map?.getOutputSizes(ImageFormat.YUV_420_888)
                ?.maxByOrNull { it.width.toLong() * it.height }
            val photoMax = map?.getOutputSizes(ImageFormat.JPEG)
                ?.maxByOrNull { it.width.toLong() * it.height }
            val array = c.get(CameraCharacteristics.SENSOR_INFO_ACTIVE_ARRAY_SIZE)
            val focal = c.get(CameraCharacteristics.LENS_INFO_AVAILABLE_FOCAL_LENGTHS)
                ?.joinToString(", ") { String.format(Locale.ROOT, "%.2f mm", it) }
                ?: getString(R.string.camera_diag_unknown)
            val physical = c.physicalCameraIds.sorted().joinToString(", ")
            fun dimensions(size: Size?): String =
                size?.let { "${it.width} × ${it.height}" } ?: getString(R.string.camera_diag_unknown)

            return buildString {
                appendLine(getString(R.string.camera_diag_selected, id))
                appendLine(getString(R.string.camera_diag_back_count, availableIds.size))
                appendLine(getString(R.string.camera_diag_focal, focal))
                appendLine(getString(R.string.camera_diag_active,
                    array?.let { "${it.width()} × ${it.height()}" } ?: getString(R.string.camera_diag_unknown)))
                appendLine(getString(R.string.camera_diag_yuv, dimensions(yuvMax)))
                appendLine(getString(R.string.camera_diag_jpeg, dimensions(photoMax)))
                if (physical.isNotEmpty()) appendLine(getString(R.string.camera_diag_physical, physical))
                appendLine()
                appendLine(getString(R.string.camera_diag_analysis, dimensions(info.analysisSizes.firstOrNull())))
                appendLine(getString(R.string.camera_diag_target_fps, st.targetFps))
                appendLine(getString(
                    if (st.autoResolution) R.string.camera_diag_auto_on else R.string.camera_diag_auto_off
                ))
                appendLine()
                append(getString(R.string.camera_diag_hud_note))
            }
        }
    }
}
