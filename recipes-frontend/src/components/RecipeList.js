import { useState } from "react";
import { useQuery } from "react-query";
import axios from "axios";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Select,
  MenuItem,
  Paper,
} from "@mui/material";

const fetchRecipes = async (sort, category) => {
  const { data } = await axios.get("http://127.0.0.1:8000/api/recipes/", {
    params: { ordering: sort, category: category || undefined },
  });
  return data;
};

export default function RecipeList() {
  const [sort, setSort] = useState("id");
  const [category, setCategory] = useState("");

  const { data: recipes, isLoading } = useQuery(["recipes", sort, category], () =>
    fetchRecipes(sort, category)
  );

  if (isLoading) return <p>Loading...</p>;

  return (
    <Paper>
      <Select value={category} onChange={(e) => setCategory(e.target.value)}>
        <MenuItem value="">Все категории</MenuItem>
        <MenuItem value="Десерты">Десерты</MenuItem>
        <MenuItem value="Первые блюда">Первые блюда</MenuItem>
        <MenuItem value="Вторые блюда">Вторые блюда</MenuItem>
        <MenuItem value="Напитки">Напитки</MenuItem>
      </Select>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {["Id", "Название", "Ингредиенты", "Категория", "Цена"].map((col) => (
                <TableCell key={col}>
                  <TableSortLabel
                    active={sort === col.toLowerCase()}
                    direction="asc"
                    onClick={() => setSort(col.toLowerCase())}
                  >
                    {col}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {recipes.map((recipe) => (
              <TableRow key={recipe.id}>
                <TableCell>{recipe.id}</TableCell>
                <TableCell>{recipe.title}</TableCell>
                <TableCell>{recipe.ingredients}</TableCell>
                <TableCell>{recipe.category}</TableCell>
                <TableCell>{recipe.price}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
