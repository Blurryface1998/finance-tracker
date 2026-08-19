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
