import { useEffect, useState } from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Box,
  Paper,
  Grid,
} from "@mui/material";
import MuiInput from "@mui/material/Input";
import { Bar, Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

// Chart.js component registration
ChartJS.register(
  ArcElement,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [insights, setInsights] = useState("");
  const [charts, setCharts] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setInsights(data.insights);
    setCharts(data.charts);
  };

  useEffect(() => {
    const mockCharts = {
      pie: {
        labels: ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Other"],
        datasets: [
          {
            data: [1200, 800, 500, 300, 200, 100],
            backgroundColor: ["#4F46E5", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#94A3B8"],
          },
        ],
      },
      bar: {
        labels: ["Jan", "Feb", "Mar", "Apr"],
        datasets: [
          {
            label: "Monthly Expenditure ($)",
            data: [3200, 2800, 1900, 1200],
            backgroundColor: "#3B82F6",
          },
        ],
      },
      top: {
        labels: ["Food", "Housing", "Transportation"],
        datasets: [
          {
            label: "Top Categories ($)",
            data: [950, 700, 430],
            backgroundColor: ["#F59E0B", "#3B82F6", "#10B981"],
          },
        ],
      },
      line: {
        labels: ["Feb", "March", "April"],
        datasets: [
          {
            label: "Cumulative Spend ($)",
            data: [1800, 4200, 6700],
            borderColor: "#10B981",
            backgroundColor: "#D1FAE5",
            fill: true,
            tension: 0.4,
          },
        ],
      },
    };

    setInsights(
      "Sample insights: You spent the most on Housing and Food. Expenditure reduced steadily over the last 4 months."
    );
    setCharts(mockCharts);
  }, []);

  return (
    <>
      <AppBar position="static" sx={{ backgroundColor: "#1976d2", boxShadow: 3 }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            RAG-powered PDF Expense Analyzer
          </Typography>
        </Toolbar>
      </AppBar>

      <Container className="app-container">
        <Box className="upload-section">
          <MuiInput
            type="file"
            onChange={(e) => {
              const target = e.target as HTMLInputElement;
              setFile(target.files?.[0] || null);
            }}
            className="upload-input"
          />
          <Button variant="contained" color="primary" onClick={handleUpload}>
            Upload PDF
          </Button>
        </Box>

        {insights && (
          <Paper className="insight-box">
            <Typography variant="h6" gutterBottom>
              Insights
            </Typography>
            <pre>{insights}</pre>
          </Paper>
        )}

        {charts && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} lg={4}>
              <Paper className="chart-card">
                <Typography variant="subtitle1" align="center">
                  Expenditure by Category
                </Typography>
                <Pie
                  data={charts.pie}
                  options={{ maintainAspectRatio: false, responsive: true }}
                  height={300}
                />
              </Paper>
            </Grid>

            <Grid item xs={12} md={6} lg={4}>
              <Paper className="chart-card">
                <Typography variant="subtitle1" align="center">
                  Monthly Expenditure
                </Typography>
                <Bar
                  data={charts.bar}
                  options={{ maintainAspectRatio: false, responsive: true }}
                  height={300}
                />
              </Paper>
            </Grid>

            <Grid item xs={12} md={6} lg={4}>
              <Paper className="chart-card">
                <Typography variant="subtitle1" align="center">
                  Top Expense Categories
                </Typography>
                <Bar
                  data={charts.top}
                  options={{
                    maintainAspectRatio: false,
                    responsive: true,
                    indexAxis: "y",
                  }}
                  height={300}
                />
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper className="chart-card">
                <Typography variant="subtitle1" align="center">
                  Cumulative Expenditure Over Time
                </Typography>
                <Line
                  data={charts.line}
                  options={{ maintainAspectRatio: false, responsive: true }}
                  height={300}
                />
              </Paper>
            </Grid>
          </Grid>
        )}
      </Container>
    </>
  );
}

export default App;