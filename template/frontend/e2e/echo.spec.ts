import { expect, test } from "@playwright/test";

test("echoes reversed and mirrored messages", async ({ page }) => {
  await page.goto("/echo");

  await page.getByLabel("Mensagem").fill("Hello");
  await page.getByLabel("Tipo de echo").selectOption("Reverse");
  await page.getByRole("button", { name: "Enviar" }).click();

  await expect(page.getByTestId("echo-result")).toHaveText("olleH");

  await page.getByLabel("Tipo de echo").selectOption("Mirror");
  await page.getByRole("button", { name: "Enviar" }).click();

  await expect(page.getByTestId("echo-result")).toHaveText("Hello | olleH");
});
