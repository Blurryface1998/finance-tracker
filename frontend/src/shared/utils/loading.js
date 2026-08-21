export const minimumLoadingTime = async (promise, minimumTime = 500) => {
  const start = Date.now();

  const result = await promise;

  const elapased = Date.now() - start;

  if (elapased < minimumTime) {
    await new Promise((resolve) => setTimeout(resolve, minimumTime - elapased));
  }
  return result;
};
