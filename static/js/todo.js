// 追蹤已檢查過的過期 todo 項目
const checkedExpiredTodos = new Set();

async function checkTodoStatus(todoId) {
  try {
    const response = await fetch(`/api/todo/${todoId}/status/`);
    if (response.ok) {
      const data = await response.json();
      return data.done;
    }
  } catch (error) {
    console.error('Error checking todo status:', error);
  }
  return false;
}

function updateProgressBarColor(progressBar, percentage) {
  let backgroundColor;
  if (percentage > 75) {
    // 綠色到淺綠色 (75-100%)
    const intensity = 40 + (percentage - 75) * 0.6; // 40-55
    backgroundColor = `hsl(120, 70%, ${intensity}%)`;
  } else if (percentage > 50) {
    // 黃綠色到綠色 (50-75%)
    const hue = 60 + (percentage - 50) * 2.4; // 60-120
    backgroundColor = `hsl(${hue}, 70%, 45%)`;
  } else if (percentage > 25) {
    // 橘色到黃色 (25-50%)
    const hue = 30 + (percentage - 25) * 1.2; // 30-60
    backgroundColor = `hsl(${hue}, 75%, 50%)`;
  } else {
    // 紅色到橘色 (0-25%)
    const hue = percentage * 1.2; // 0-30
    backgroundColor = `hsl(${hue}, 80%, 50%)`;
  }
  
  progressBar.style.backgroundColor = backgroundColor;
  progressBar.className = 'progress-bar progress-bar-striped progress-bar-animated';
}

async function updateCountdowns() {
  const countdowns = document.querySelectorAll('.countdown');
  const progressBars = document.querySelectorAll('.progress-bar');

  // 更新倒數計時
  for (const el of countdowns) {
    const deadline = new Date(el.dataset.deadline);
    const now = new Date();
    const diff = deadline - now;
    const todoId = el.dataset.todoId;

    if (diff <= 0) {
      // 檢查是否有 checkTodoStatus 功能（首頁才有）且尚未檢查過
      if (todoId && typeof checkTodoStatus === 'function' && !checkedExpiredTodos.has(todoId)) {
        const isDone = await checkTodoStatus(todoId);
        checkedExpiredTodos.add(todoId); // 標記為已檢查
        if (isDone) {
          el.className = 'badge bg-success';
          el.textContent = '已完成';
        } else {
          el.className = 'badge bg-danger';
          el.textContent = '已截止';
        }
      } else if (!todoId || typeof checkTodoStatus !== 'function') {
        el.textContent = "已截止";
      }
    } else {
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);
      el.textContent = `${hours}時 ${minutes}分 ${seconds}秒`;
    }
  }

  // 更新進度條
  for (const progressBar of progressBars) {
    const created = new Date(progressBar.dataset.created);
    const deadline = new Date(progressBar.dataset.deadline);
    const now = new Date();
    const todoId = progressBar.dataset.todoId;

    const totalTime = deadline - created;
    const remainingTime = deadline - now;
    
    if (remainingTime <= 0) {
      // 檢查是否完成（首頁才有此功能）且尚未檢查過
      if (todoId && typeof checkTodoStatus === 'function' && !checkedExpiredTodos.has(todoId)) {
        const isDone = await checkTodoStatus(todoId);
        checkedExpiredTodos.add(todoId); // 標記為已檢查
        if (isDone) {
          progressBar.style.width = '100%';
          progressBar.style.backgroundColor = '#28a745';
          progressBar.className = 'progress-bar';
        } else {
          progressBar.style.width = '0%';
          progressBar.style.backgroundColor = '#dc3545';
          progressBar.className = 'progress-bar';
        }
      } else {
        // 沒有檢查功能或已檢查過，直接顯示過期狀態
        progressBar.style.width = '0%';
        progressBar.style.backgroundColor = '#dc3545';
        progressBar.className = 'progress-bar';
      }
    } else {
      const percentage = Math.max(0, (remainingTime / totalTime) * 100);
      progressBar.style.width = percentage + '%';
      updateProgressBarColor(progressBar, percentage);
    }
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
  setInterval(updateCountdowns, 1000);
  updateCountdowns();
});
