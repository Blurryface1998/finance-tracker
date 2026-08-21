export function formatServerError(message, fieldName, data) {
  let formattedMessage = message.replace(/^Value error,\s*/i, "");

  if (fieldName === "email") {
    formattedMessage = formattedMessage.replace(
      /^Value is not a valid email address/i,
      `${data.email} is not a valid email address`,
    );
  }

  return formattedMessage;
}

export const handleFormError = (err, setError, data) => {
  const errorData = err.response?.data;

  if (!errorData) {
    setError("root.server", {
      type: "server",
      message: "Something went wrong. Please try again.",
    });

    console.error("Network or unexpected error: ", err);
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

  return errorData;
};
