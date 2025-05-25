use pyo3::prelude::*;
use rosu_pattern_detector::calc::get_patterns;
use serde_json;

#[pyfunction]
fn get_patterns_python(path: String) -> PyResult<String> {
    let patterns = get_patterns(&path)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    let json = serde_json::to_string(&patterns)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    Ok(json)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rosu_pattern_detector_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_patterns_python, m)?)?;
    Ok(())
}
