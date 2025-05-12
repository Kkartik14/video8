import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

export const generateVideo = async (prompt, model, use_modular = true) => {
  try {
    console.log(`Sending request to ${API_URL}/generate with model: ${model}, modular: ${use_modular}`);
    
    const response = await axios.post(`${API_URL}/generate`, {
      prompt,
      model,
      use_modular
    });
    
    console.log('API response:', response.data);
    return response.data;
  } catch (error) {
    console.error('API error:', error);
    
    if (error.code === 'ERR_NETWORK' || error.code === 'ERR_CONNECTION_REFUSED') {
      throw new Error(`Cannot connect to the backend server at ${API_URL}. Please make sure it's running.`);
    }
    
    throw error.response?.data?.detail || error.message || 'Failed to generate video';
  }
};

export const getVideoData = async (videoPath) => {
  try {
    const fullPath = videoPath.startsWith('http') 
      ? videoPath 
      : `${API_URL}/${videoPath.replace(/^\//, '')}`;
      
    console.log(`Fetching video from: ${fullPath}`);
    
    const response = await axios.get(fullPath, {
      responseType: 'blob',
    });
    
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Error fetching video:', error);
    throw error.response?.data?.detail || error.message || 'Failed to get video data';
  }
};

export const getScriptData = async (scriptPath) => {
  try {
    const fullPath = scriptPath.startsWith('http') 
      ? scriptPath 
      : `${API_URL}/${scriptPath.replace(/^\//, '')}`;
      
    console.log(`Fetching script from: ${fullPath}`);
    
    const response = await axios.get(fullPath, {
      responseType: 'text',
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching script:', error);
    throw error.response?.data?.detail || error.message || 'Failed to get script data';
  }
}; 