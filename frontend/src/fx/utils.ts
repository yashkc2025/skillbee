export function getTodayName(): string {
  const today = new Date();
  return today.toLocaleDateString('en-US', { weekday: 'long' });
}

export function searchQuery<T>(
  items: T[],
  query: string,
  searchFields: (keyof T)[]
): T[] {
  if (!query) return items;
  const lowerQuery = query.toLowerCase();
  return items.filter(item =>
    searchFields.some(field => {
      const value = item[field];
      if (typeof value === 'string') {
        return value.toLowerCase().includes(lowerQuery);
      }
      if (value instanceof Date) {
        return value.toISOString().includes(lowerQuery);
      }
      if (typeof value === 'number') {
        return value.toString().includes(lowerQuery);
      }
      return false;
    })
  );
}
export const generateLabel = (key: string) => {
  return key
    .replace(/_/g, ' ')                 // replace underscores with spaces
    .replace(/([a-z])([A-Z])/g, '$1 $2') // insert space before capital letters
    .replace(/\b\w/g, char => char.toUpperCase()) // capitalize first letter of each word
}

type AnyObject = { [key: string]: any };

export function flattenObject(obj: AnyObject, parentKey = '', result: AnyObject = {}): AnyObject {
  for (const key in obj) {
    if (!obj.hasOwnProperty(key)) continue;

    const newKey = parentKey ? `${parentKey}_${key}` : key;

    if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
      flattenObject(obj[key], newKey, result);
    } else {
      result[newKey] = obj[key];
    }
  }

  return result;
}
