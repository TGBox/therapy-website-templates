export function greet(name: string): string {
  return `Hello, ${name}! Welcome to therapy-website-templates.`;
}

if (process.env.NODE_ENV !== "test") {
  console.log(greet("World"));
}