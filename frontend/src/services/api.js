import axios from "axios";


const API_URL =
  import.meta.env.VITE_API_URL ; 

export async function sendMessage(question, password = null) {
  console.log("sathish" + question , password);
  const response = await axios.post(`${API_URL}/chat`, {
      question,
      password,
  });

  let data;
  try {
    data = await response.data;
    console.log("data from backend", data);
  } catch(error){
    const detail = error.response?.data?.detail || "An error occurred while processing your request.";
    console.error("Error from backend:", detail);

      throw new Error(detail);
  }

  return data;
}