import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import AboutPage from "./pages/AboutPage";
import EchoPage from "./pages/EchoPage";
import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";
[[#if database]]
import NotesPage from "./pages/NotesPage";
[[/endif]]

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="echo" element={<EchoPage />} />
          [[#if database]]
          <Route path="notes" element={<NotesPage />} />
          [[/endif]]
          <Route path="about" element={<AboutPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
