import { useToast } from "vue-toastification";

const toast = useToast();

export async function submitForm(address, event) {
  event.preventDefault(); // Prevents full page reload

  const formData = new FormData(event.target); // Collects all form data

  try {
    const response = await fetch(address, {
      method: "POST",
      body: formData,
      credentials: "include",
    });

    if (response.status >= 200 && response.status < 300) {
      const data = await response.json();
      if (data.redirect) {
        window.location.href = data.redirect;
      }
      if (data.message) {
        toast.success(data.message);
      }
    } else if (response.status >= 400) {
      const data = await response.json();
      if (data.error) {
        toast.error(data.error);
      }
      if (data.message) {
        toast.error(data.message);
      }
    } else {
      return response;
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    throw error;
  }
}

export async function postData(address, data) {
  try {
    const response = await fetch(address, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
      credentials: "include",
    });

    if (response.ok) {
      const responseData = await response.json();

      if (responseData.message) {
        toast.success(responseData.message);
      }
      if (responseData.redirect) {
        window.location.href = responseData.redirect;
      }
      return responseData;
    } else {
      console.error("Request Failed");
      return response;
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    throw error;
  }
}

export async function fetchData(address, q) {
  const queryString = new URLSearchParams(q).toString();
  const urlWithQuery = queryString ? `${address}?${queryString}` : address;

  const response = await fetch(urlWithQuery, {
    method: "GET",
    credentials: "include",
  });

  if (response.status === 200) {
    const data = await response.json();
    return data;
  } else {
    throw new Error(`Failed to fetch data. Status: ${response.status}`);
  }
}

export async function downloadFile(address) {
  const response = await fetch(address, {
    method: "GET",
    headers: {
      "Access-Control-Expose-Headers": "Content-Disposition",
    },
    credentials: "include",
  });

  if (response.status != 200) {
    toast.error("Failed to download");
  }
  console.log(response.headers);
  const filename = response.headers.get("content-disposition");
  if (filename) {
    console.log(1);
    const filenameMatch = filename.match(
      /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
    );
    let fileName = "";
    if (filenameMatch && filenameMatch[1]) {
      fileName = filenameMatch[1].replace(/["']/g, "");
    }

    console.log(fileName);

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
}
