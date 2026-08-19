export async function onSubmit({ data, response }) {
  console.log("DATA being sent:", data);
  try {
    await response(data);

    alert("Register Sucessful!");
  } catch (err) {
    const errorData = err.response?.data;
    if (!errorData) {
      console.error("Network or unexpected error:", err);
      return;
    }
    if (Array.isArray(errorData.detail)) {
      errorData.detail.forEach((error) => {
        const fieldName = error.loc[error.loc.length - 1];

        setError(fieldName, {
          type: "server",
          message: formatServerError(error.msg, fieldName, data),
        });
      });
    }
    if (errorData.error?.code === "email_registered") {
      setError("email", {
        type: "server",
        message: errorData.error.message,
      });
    }
  }
}
