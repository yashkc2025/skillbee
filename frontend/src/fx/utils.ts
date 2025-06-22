export function getTodayName(): string {
  const today = new Date();
  return today.toLocaleDateString('en-US', { weekday: 'long' });
}
