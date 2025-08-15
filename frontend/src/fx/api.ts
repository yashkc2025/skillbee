import { useToast } from "vue-toastification";


export async function submitForm(address: string, event) {
  const toast = useToast();
  const token = localStorage.getItem("authToken");

  event.preventDefault(); // Prevents full page reload

  const formData = new FormData(event.target); // Collects all form data

  try {
    const response = await fetch(address, {
      method: "POST",
      body: formData,
      credentials: "include",
      headers: {
        "Authorization": `Bearer ${token}`,
      }
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

export async function postData(address: string, data: Object) {
  const toast = useToast();
  const token = localStorage.getItem("authToken");

  try {
    const response = await fetch(address, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
      credentials: "include",
    });

    if (response.status === 200 || response.status === 201) {
      const responseData = await response.json();

      const message = typeof responseData?.message === 'string' && responseData.message.trim()
        ? responseData.message
        : "Updated";

      toast.success(message);

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

export async function updateData(address: string, data: Object) {
  const toast = useToast();
  const token = localStorage.getItem("authToken");

  try {
    const response = await fetch(address, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
      credentials: "include",
    });
    if (response.status >= 400) {
      const data = await response.json();
      if (data.error) {
        toast.error(data.error);
      }
      if (data.message) {
        toast.error(data.message);
      }
    }

    if (response.status === 200 || response.status === 201) {
      const responseData = await response.json();
      console.log(responseData)

      const message = typeof responseData?.message === 'string' && responseData.message.trim()
        ? responseData.message
        : "Updated";

      toast.success(message);


      if (responseData.redirect) {
        window.location.href = responseData.redirect;
      }


    } else {
      console.error("Request Failed");
      return response;
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    throw error;
  }
}

export async function deleteData(address: string, data: Object) {
  const token = localStorage.getItem("authToken");

  try {
    const response = await fetch(address, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Convert the data object to a JSON string
      credentials: "include",
    });

    if (response.status === 200 || response.status === 201) {
      const responseData = await response.json();

      if (responseData.message) {
        window.location.reload();
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

export async function fetchData(address: string, q?: Object) {
  const token = localStorage.getItem("authToken");
  const toast = useToast();

  const queryString = new URLSearchParams(q).toString();
  const urlWithQuery = queryString ? `${address}?${queryString}` : address;

  const response = await fetch(urlWithQuery, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (response.status === 200) {
    const data = await response.json();
    return data;
  } else {
    toast.error("Error occured");

    throw new Error(`Failed to fetch data. Status: ${response.status}`);
  }
}

export async function downloadFile(address: string) {
  const token = localStorage.getItem("authToken");

  const toast = useToast();

  const response = await fetch(address, {
    method: "GET",
    headers: {
      "Access-Control-Expose-Headers": "Content-Disposition",
      "Authorization": `Bearer ${token}`,
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
