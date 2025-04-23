let config = {};

export const loadConfig = async () => {
  try {
    const response = await fetch('/config.json');
    if (!response.ok) throw new Error('Failed to load config');
    const data = await response.json();
    config = data;
  } catch (error) {
    console.error("Error loading config:", error);
  }
};

export const getConfig = (key) => config[key];
