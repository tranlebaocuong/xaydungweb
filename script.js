const lessonButtons = document.getElementById('lessonButtons');
const lessonTitleElement = document.getElementById('lessonTitle');
const lessonOutput = document.getElementById('lessonOutput');
const lessonPlaceholder = document.getElementById('lessonPlaceholder');
const appShell = document.querySelector('.app-shell');
const menuToggle = document.getElementById('menuToggle');
const lessonPanel = document.getElementById('lessonPanel');
let activeButton = null;
const viewHistory = [];

function setMenuOpen(isOpen) {
  appShell?.classList.toggle('menu-open', isOpen);
  menuToggle?.setAttribute('aria-expanded', String(isOpen));
}

function toggleMenu() {
  setMenuOpen(!appShell?.classList.contains('menu-open'));
}

function isMobileMenuLayout() {
  return window.matchMedia('(max-width: 820px)').matches;
}

function closeMenuOnMobile() {
  if (isMobileMenuLayout()) {
    setMenuOpen(false);
  }
}

menuToggle?.addEventListener('click', (event) => {
  event.stopPropagation();
  toggleMenu();
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    setMenuOpen(false);
  }
});

document.addEventListener('click', (event) => {
  if (!isMobileMenuLayout() || !appShell?.classList.contains('menu-open')) {
    return;
  }
  const target = event.target;
  if (lessonPanel?.contains(target) || menuToggle?.contains(target)) {
    return;
  }
  setMenuOpen(false);
});

// Hard-coded lesson map (client-side) based on workspace structure.
const structure = {
  'NGÀNH ĐỒNG': {
    sections: {
      'MỞ MẮT': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/oanh_vũ/mở_mắt/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            basePath: 'data/oanh_vũ/mở_mắt/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'VĂN NGHỆ': {
            basePath: 'data/oanh_vũ/mở_mắt/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt']
          }
        }
      },
      'CÁNH MỀM': {
        sections: {
          'PHẬT PHÁP': {
            introFile: 'data/oanh_vũ/cánh_mềm/phật pháp/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            introFile: 'data/oanh_vũ/cánh_mềm/hoạt_động_thanh_niên_và_xã_hội/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt','bài_15.txt','bài_16.txt','bài_17.txt','bài_18.txt','bài_19.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/oanh_vũ/cánh_mềm/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt']
          }
        }
      },
      'CHÂN CỨNG': {
        sections: {
          'PHẬT PHÁP': {
            introFile: 'data/oanh_vũ/chân_cứng/phật pháp/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/chân_cứng/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            introFile: 'data/oanh_vũ/chân_cứng/hoạt_động_thanh_niên_và_xã_hội/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/chân_cứng/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt','bài_15.txt','bài_16.txt','bài_17.txt','bài_18.txt','bài_19.txt','bài_20.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/oanh_vũ/chân_cứng/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/chân_cứng/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt']
          }
        }
      },
      'TUNG BAY': {
        sections: {
          'PHẬT PHÁP': {
            introFile: 'data/oanh_vũ/tung_bay/phật pháp/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/tung_bay/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt','bài_15.txt','bài_16.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            introFile: 'data/oanh_vũ/tung_bay/hoạt_động_thanh_niên_và_xã_hội/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/tung_bay/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt','bài_15.txt','bài_16.txt','bài_17.txt','bài_18.txt','bài_19.txt','bài_20.txt','bài_21.txt','bài_22.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/oanh_vũ/tung_bay/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/tung_bay/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt']
          }
        }
      }
    }
  },
  'NGÀNH THIẾU': {
    sections: {
      'HƯỚNG THIỆN': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/ngành_thiếu/hướng_thiện/phật_pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN': {
            sections: {
              'CỨU THƯƠNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/cứu_thương/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/cứu_thương', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt'] },
              'DẤU ĐI ĐƯỜNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dấu_đi_đường/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dấu_đi_đường', files: ['bài_1.txt','bài_2.txt'] },
              'DỰNG LỀU': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dựng_lều/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dựng_lều', files: ['bài_1.txt','bài_2.txt'] },
              'GÚT DÂY': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/gút_dây/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/gút_dây', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'] },
              'PHƯƠNG HƯỚNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/phương_hướng/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/phương_hướng', files: ['bài_1.txt','bài_2.txt'] },
              'MẬT THƯ': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/mật_thư/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/mật_thư', files: ['bài_1.txt','bài_2.txt'] },
              'THƯỜNG THỨC': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/thường_thức/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/thường_thức', files: ['bài_1.txt'] },
              'TRUYỀN TIN': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/truyền_tin/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/truyền_tin', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt'] }
            }
          },
          'HOẠT ĐỘNG XÃ HỘI': {
            introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_xã_hội/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/ngành_thiếu/hướng_thiện/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/hướng_thiện/văn_nghệ',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','danh_sách_bài_hát.txt'
            ]
          }
        }
      },
      'SƠ THIỆN': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/ngành_thiếu/sơ_thiện/phật_pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN': {
            sections: {
              'CỨU THƯƠNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/cứu_thương/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/cứu_thương', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt'] },
              'DẤU ĐI ĐƯỜNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dấu_đi_đường/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dấu_đi_đường', files: ['bài_1.txt','bài_2.txt'] },
              'DỰNG LỀU': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dựng_lều/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dựng_lều', files: ['bài_1.txt','bài_2.txt'] },
              'GÚT DÂY': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/gút_dây/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/gút_dây', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'] },
              'PHƯƠNG HƯỚNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/phương_hướng/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/phương_hướng', files: ['bài_1.txt','bài_2.txt'] },
              'MẬT THƯ': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/mật_thư/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/mật_thư', files: ['bài_1.txt','bài_2.txt'] },
              'THƯỜNG THỨC': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/thường_thức/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/thường_thức', files: ['bài_1.txt'] },
              'TRUYỀN TIN': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/truyền_tin/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/truyền_tin', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt'] }
            }
          },
          'HOẠT ĐỘNG XÃ HỘI': {
            introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_xã_hội/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/ngành_thiếu/sơ_thiện/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/sơ_thiện/văn_nghệ',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','danh_sách_bài_hát.txt'
            ]
          }
        }
      }
    }
  }
};

function pushView(viewFn) {
  viewHistory.push(viewFn);
}

function goBack() {
  if (viewHistory.length <= 1) return;
  viewHistory.pop();
  const previous = viewHistory[viewHistory.length - 1];
  previous();
}

function clearButtons() {
  lessonButtons.innerHTML = '';
}

function setActiveButton(button) {
  if (activeButton) activeButton.classList.remove('active');
  activeButton = button;
  if (activeButton) activeButton.classList.add('active');
}

function setLessonTitle(title) {
  const normalizedTitle = title.replace(/\s+/g, ' ').trim();
  lessonTitleElement.textContent = normalizedTitle;
  lessonTitleElement.classList.remove('title-long', 'title-very-long');

  if (normalizedTitle.length >= 72) {
    lessonTitleElement.classList.add('title-very-long');
  } else if (normalizedTitle.length >= 48) {
    lessonTitleElement.classList.add('title-long');
  }
}

function createButton(label, onClick) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'lesson-button';
  btn.textContent = label;
  btn.title = label;
  btn.addEventListener('click', () => onClick(btn));
  return btn;
}

function createBackButton() {
  if (viewHistory.length <= 1) return null;
  return createButton('« Quay lại', () => goBack());
}

function getFallbackTitle(filename) {
  const basename = filename.split('/').pop().split('\\').pop();
  return basename.replace('bài_', 'Bài ').replace('.txt', '');
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isHeadingLine(line) {
  const trimmed = line.trim();
  if (!trimmed) return false;
  if (/^[IVXLCDM]+\s*[-./]\s*/i.test(trimmed)) return true;
  if (/^[0-9]+\s*[-.)]\s+/.test(trimmed)) return true;
  if (/^[a-zA-Z]\s*[-./)]\s*/.test(trimmed)) return true;
  return trimmed === trimmed.toUpperCase() && /[A-ZÀ-ỸỤƠƯÁÀẠẢẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]/.test(trimmed) && trimmed.length > 2;
}

function resolveImagePath(baseDir, src) {
  const candidates = getImagePathCandidates(baseDir, src);
  return candidates[0] || src;
}

function getImagePathCandidates(baseDir, src) {
  if (!src || /^(https?:|data:|\/)/i.test(src)) {
    return [src];
  }
  if (!baseDir || baseDir === '.') {
    return [src];
  }

  const normalizedSrc = src.replace(/\\/g, '/').replace(/^\.\/+/, '');
  if (/^ảnh_bài_/i.test(normalizedSrc)) {
    return [`${baseDir}/ảnh/${normalizedSrc}`, `${baseDir}/${normalizedSrc}`];
  }
  return [`${baseDir}/${normalizedSrc}`];
}

function toImageSrc(path) {
  if (!path || /^(https?:|data:)/i.test(path)) {
    return path;
  }
  return encodeURI(path);
}

function imageFallbackAttributes(baseDir, rawSrc) {
  const candidates = getImagePathCandidates(baseDir, rawSrc).map(toImageSrc);
  if (candidates.length < 2) {
    return { src: candidates[0] || '', attrs: '' };
  }
  return {
    src: candidates[0],
    attrs: ` data-fallback-src="${escapeHtml(candidates[1])}" onerror="useImageFallback(this)"`
  };
}

function useImageFallback(img) {
  const fallbackSrc = img.getAttribute('data-fallback-src');
  if (!fallbackSrc) {
    return;
  }
  img.removeAttribute('data-fallback-src');
  img.src = fallbackSrc;
}

function isImageMarkdownLine(line) {
  return /^\s*!\[[^\]]*\]\([^)]+\)\s*$/.test(line);
}

function isContentStartLine(line) {
  const trimmed = line.trim();
  if (!trimmed) return false;
  if (isImageMarkdownLine(trimmed)) return true;
  if (/^\(.+\)$/.test(trimmed)) return true;
  if (/^[IVXLCDM]+\s*[-./]\s*/i.test(trimmed)) return true;
  if (/^[A-Z]\s*[-./)]\s*/.test(trimmed)) return true;
  if (/^[0-9]+\s*[-.)]\s+/.test(trimmed)) return true;
  if (/^[-*+]\s+/.test(trimmed)) return true;
  return false;
}

function hasLowercaseLetter(text) {
  return /[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/.test(text);
}

function isUppercaseTitleLine(text) {
  const letters = text.replace(/[^A-Za-zÀ-ỹĐđ]/g, '');
  return letters.length > 0 && letters === letters.toUpperCase();
}

function isLikelyTitleContinuationLine(text) {
  const withoutParentheses = text.replace(/\([^)]*\)/g, '');
  const letters = withoutParentheses.replace(/[^A-Za-zÀ-ỹĐđ]/g, '');
  const hasLessonPart = /\(\s*(?:\d+\s*)?tiết\s*\d*\s*\)/i.test(text);
  if (!letters.length) {
    return hasLessonPart;
  }
  return letters === letters.toUpperCase() && (hasLessonPart || text.length <= 70);
}

function parseLessonText(text, fallbackTitle = 'Giới thiệu') {
  const lines = text.split(/\r?\n/);
  const firstContentLine = lines.findIndex(line => line.trim().length > 0);
  if (firstContentLine < 0) {
    return { title: fallbackTitle, content: '' };
  }

  const titleLines = [];
  let contentStart = firstContentLine;

  for (let i = firstContentLine; i < lines.length; i += 1) {
    const trimmed = lines[i].trim();
    if (!trimmed) {
      contentStart = i + 1;
      break;
    }
    if (titleLines.length > 0 && isLikelyTitleContinuationLine(trimmed)) {
      titleLines.push(trimmed);
      contentStart = i + 1;
      continue;
    }
    if (titleLines.length > 0 && isContentStartLine(trimmed)) {
      contentStart = i;
      break;
    }
    if (titleLines.length > 0 && isUppercaseTitleLine(titleLines[titleLines.length - 1]) && hasLowercaseLetter(trimmed)) {
      contentStart = i;
      break;
    }
    if (titleLines.length >= 4) {
      contentStart = i;
      break;
    }
    titleLines.push(trimmed);
    contentStart = i + 1;
  }

  const title = titleLines.join(' ').replace(/\s+/g, ' ').trim() || fallbackTitle;
  const content = lines.slice(contentStart).join('\n').trim();
  return { title, content };
}

function formatLessonHTML(text, baseDir) {
  const lines = text.split(/\r?\n/);
  const htmlLines = [];
  let inList = false;
  const imageMarkdown = /^\s*!\[([^\]]*)\]\(([^)]+)\)\s*$/;
  const imageLine = /^\s*(?:!IMAGE|IMAGE|HÌNH ẢNH)[:\s]+(.+)$/i;
  const listItem = /^\s*[-*+]\s+(.+)$/;

  const closeList = () => {
    if (inList) {
      htmlLines.push('</ul>');
      inList = false;
    }
  };

  for (const line of lines) {
    if (line.trim() === '') {
      closeList();
      htmlLines.push('<div class="lesson-spacer"></div>');
      continue;
    }

    const markdownMatch = line.match(imageMarkdown);
    if (markdownMatch) {
      closeList();
      const alt = escapeHtml(markdownMatch[1].trim() || 'Hình ảnh');
      const rawSrc = markdownMatch[2].trim();
      const image = imageFallbackAttributes(baseDir, rawSrc);
      htmlLines.push(`<div class="lesson-image-wrapper"><img src="${escapeHtml(image.src)}" alt="${alt}" class="lesson-image"${image.attrs} /><p class="lesson-image-caption">${alt}</p></div>`);
      continue;
    }

    const imageLineMatch = line.match(imageLine);
    if (imageLineMatch) {
      closeList();
      const image = imageFallbackAttributes(baseDir, imageLineMatch[1].trim());
      htmlLines.push(`<div class="lesson-image-wrapper"><img src="${escapeHtml(image.src)}" alt="Hình ảnh" class="lesson-image"${image.attrs} /></div>`);
      continue;
    }

    const listMatch = line.match(listItem);
    if (listMatch) {
      if (!inList) {
        htmlLines.push('<ul class="lesson-list-items">');
        inList = true;
      }
      htmlLines.push(`<li>${escapeHtml(listMatch[1].trim())}</li>`);
      continue;
    }

    closeList();
    const escaped = escapeHtml(line);
    if (isHeadingLine(line)) {
      htmlLines.push(`<p class="lesson-heading"><strong>${escaped}</strong></p>`);
      continue;
    }
    htmlLines.push(`<p>${escaped}</p>`);
  }

  closeList();
  return htmlLines.join('');
}

async function fetchTitleFromFile(path) {
  if (window.location.protocol === 'file:') return getFallbackTitle(path);
  try {
    const resp = await fetch(encodeURI(path));
    if (!resp.ok) return getFallbackTitle(path);
    const txt = await resp.text();
    return parseLessonText(txt, getFallbackTitle(path)).title;
  } catch {
    return getFallbackTitle(path);
  }
}

async function loadLesson(path, button) {
  setActiveButton(button);
  closeMenuOnMobile();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.remove('hidden');
  lessonPlaceholder.classList.add('hidden');
  lessonOutput.textContent = 'Đang tải nội dung...';

  if (window.location.protocol === 'file:') {
    setLessonTitle(getFallbackTitle(path));
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.textContent = 'Trang đang được mở trực tiếp từ file. Vui lòng chạy server tĩnh (ví dụ: python -m http.server) và truy cập lại trang qua http://localhost.';
    return;
  }

  try {
    const resp = await fetch(encodeURI(path));
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const txt = await resp.text();
    const { title, content } = parseLessonText(txt, getFallbackTitle(path));
    const lessonDir = path.includes('/') ? path.slice(0, path.lastIndexOf('/')) : '.';
    setLessonTitle(title);
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.innerHTML = content ? formatLessonHTML(content, lessonDir) : '<p>[Không có nội dung khác ngoài tiêu đề]</p>';
  } catch (err) {
    setLessonTitle(getFallbackTitle(path));
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.textContent = `Lỗi khi tải nội dung: ${err.message}`;
  }
}

async function appendLessonButtons(basePath, files) {
  // Ensure bài_7 is included for gút_dây (some builds missed it)
  const fileList = Array.isArray(files) ? files.slice() : [];
  if (basePath && basePath.includes('gút_dây') && !fileList.includes('bài_7.txt')) {
    fileList.push('bài_7.txt');
  }

  for (const f of fileList) {
    const rel = basePath === '.' ? f : `${basePath}/${f}`;
    const title = await fetchTitleFromFile(rel);
    lessonButtons.appendChild(createButton(title, (btn) => loadLesson(rel, btn)));
  }
}

async function showLessonsList(basePath, files) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  await appendLessonButtons(basePath, files);

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showSectionIntro(introPath, basePath, files) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.remove('hidden');
  lessonPlaceholder.classList.add('hidden');

  if (window.location.protocol === 'file:') {
    lessonOutput.textContent = 'Trang đang được mở trực tiếp từ file.';
    const back = createBackButton();
    if (back) lessonButtons.appendChild(back);
    return;
  }

  try {
    const resp = await fetch(encodeURI(introPath));
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const txt = await resp.text();
    const { title, content } = parseLessonText(txt, 'Giới thiệu');
    const introDir = introPath.includes('/') ? introPath.slice(0, introPath.lastIndexOf('/')) : '.';
    setLessonTitle(title);
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.innerHTML = content ? formatLessonHTML(content, introDir) : '<p>[Không có nội dung khác ngoài tiêu đề]</p>';
  } catch (err) {
    lessonOutput.textContent = `Lỗi khi tải giới thiệu: ${err.message}`;
  }

  if (files && files.length > 0) {
    await appendLessonButtons(basePath, files);
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

function showSections(sections) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, info] of Object.entries(sections)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (info.introFile) {
        await navigate(() => showSectionIntro(info.introFile, info.basePath, info.files || []));
      } else if (info.sections) {
        await navigate(() => showSections(info.sections));
      } else if (info.files) {
        await navigate(() => showLessonsList(info.basePath, info.files));
      }
    }));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showCategories(sections) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, info] of Object.entries(sections)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (info.introFile) {
        await navigate(() => showSectionIntro(info.introFile, info.basePath, info.files || []));
      } else if (info.sections) {
        await navigate(() => showSections(info.sections));
      } else if (info.files) {
        await navigate(() => showLessonsList(info.basePath, info.files));
      }
    }));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showRoot() {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, group] of Object.entries(structure)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (group.sections) {
        await navigate(() => showCategories(group.sections));
      } else if (group.files) {
        await navigate(() => showLessonsList(group.basePath, group.files));
      }
    }));
  }
}

async function navigate(viewFn) {
  viewHistory.push(viewFn);
  await viewFn();
}

function init() {
  viewHistory.length = 0;
  navigate(showRoot);
}

init();

