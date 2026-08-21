import { minimumLoadingTime } from "./loading";

export const submitWithLoading = async ({
  request,
  setLoading,
  clearErrors,
}) => {
  setLoading(true);
  clearErrors("root");

  try {
    return await minimumLoadingTime(request());
  } finally {
    setLoading(false);
  }
};
