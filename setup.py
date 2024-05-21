import glob
import hashlib
import io
import os
import pathlib
import re
import shutil
import zipfile


_SHA256Hash = str
_LibraryContent = tuple[re.Pattern[str], _SHA256Hash]
_Library = tuple[pathlib.Path, list[_LibraryContent]]


def _verify_sha256_hash(data: bytes, expected: str):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest() == expected


def _verify_content(
    content: _LibraryContent, parent: zipfile.ZipFile
) -> Exception | None:
    pattern, sha256 = content

    files = [
        filename for filename in parent.namelist() if re.fullmatch(pattern, filename)
    ]
    if len(files) == 0:
        return FileNotFoundError(
            f"No file matching the pattern '{pattern}' was found in the archive"
        )
    elif len(files) != 1:
        return FileNotFoundError(
            f"{len(files)} files matching the pattern '{pattern}' were found in the archive"
        )

    file = files[0]
    with parent.open(file) as f:
        file_bytes = f.read()
        if not _verify_sha256_hash(file_bytes, sha256):
            return ValueError(f"Hash mismatch for {file}")


def _verify_library(library: _Library):
    path, contents = library

    if not path.exists():
        raise FileNotFoundError(f"The specified library path does not exist: {path}")

    with open(path, "rb") as f, zipfile.ZipFile(io.BytesIO(f.read()), "r") as zip_file:
        exceptions = [
            exception
            for exception in [
                _verify_content(content, zip_file) for content in contents
            ]
            if exception is not None
        ]
        if len(exceptions) != 0:
            error_messages = "; ".join(str(e) for e in exceptions)
            raise ExceptionGroup(
                "Multiple verification errors occurred: " + error_messages, exceptions
            )


libraries: list[_Library] = [
    (
        pathlib.Path("3rd_party/ul_NCP167AMX330TBG.zip"),
        [
            (
                re.compile(r"KiCADv6/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.kicad_sym"),
                "ba3262e20aba960309ea7f405cb4ac15662ab00ed9e0acd686bad9f8468fa383",
            ),
            (
                re.compile(
                    r"KiCADv6/footprints\.pretty/XDFN4_1X1_711AJ_ONS\.kicad_mod"
                ),
                "8a6c17f1985cbf3e110c93fdece9cab754fedfff27bd612bedcb2464c3a02dd4",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/ul_2171790001.zip"),
        [
            (
                re.compile(r"KiCADv6/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.kicad_sym"),
                "5af652fd7901813f653c5aa65c51c81227b191e688f94f7cd08e41e5b74cb35e",
            ),
            (
                re.compile(r"KiCADv6/footprints\.pretty/2171790001_MOL\.kicad_mod"),
                "7309c34f68cca23daf23a16d6ca0b9f60f4c8d939e589655fa3ab12ad6391ff5",
            ),
            (
                re.compile(r"2171790001\.stp"),
                "413570c4766b2c88fffffaa8c87c7a4e65dd61550dd9700f9fe5feba5daf01b7",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_AD8403ARUZ1-REEL.zip"),
        [
            (
                re.compile(r"AD8403ARUZ1-REEL/KiCad/AD8403ARUZ1-REEL\.kicad_sym"),
                "7ffd4665412e1365d74a6ffbe1722d706f34480c310b3a2bc92d2f39ead0505c",
            ),
            (
                re.compile(r"AD8403ARUZ1-REEL/KiCad/SOP65P640X120-24N\.kicad_mod"),
                "6da444fa362a93a50d4b4cca09cbd936a2988c40fcaabccba15997c180879473",
            ),
            (
                re.compile(r"AD8403ARUZ1-REEL/3D/AD8403ARUZ1-REEL\.stp"),
                "531ea6cf5fad798ee00b37429d4dfa3dce9d677cdc2492a1e5dc11e624a775e2",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_ADG801BRTZ-REEL7.zip"),
        [
            (
                re.compile(r"ADG801BRTZ-REEL7/KiCad/ADG801BRTZ-REEL7\.kicad_sym"),
                "08cdbaacc750edb167343029685ea4f22cf0066b7526e728e0550bb1cdfecd49",
            ),
            (
                re.compile(r"ADG801BRTZ-REEL7/KiCad/SOT95P280X145-6N\.kicad_mod"),
                "80d29e079968e4515761f9681b484985a007dad5ef0518a9b400d7cec689d581",
            ),
            (
                re.compile(r"ADG801BRTZ-REEL7/3D/ADG801BRTZ-REEL7\.stp"),
                "f44508dfccc3e09e3621e6790193a5b3930335bbac1efcbc8ff6425c82e4db50",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_AWSCR-12.00CELA-C33-T3.zip"),
        [
            (
                re.compile(
                    r"AWSCR-12.00CELA-C33-T3/KiCad/AWSCR-12_00CELA-C33-T3\.kicad_sym"
                ),
                "c76284816b0987d3b089de7559b73b042092913c173acf60a72a74fe0641f8ff",
            ),
            (
                re.compile(
                    r"AWSCR-12.00CELA-C33-T3/KiCad/AWSCR1200CELAC33T3\.kicad_mod"
                ),
                "a1eded293c7d696bee23449b43ab5a7d9b775050cb321abd7a6d8249f23dee9a",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_DS4424N+T&R.zip"),
        [
            (
                re.compile(r"DS4424N\+T&R/KiCad/DS4424N\+T&R\.kicad_sym"),
                "51daf99f44e625901b89760704761d74b6422363e2d685339a4e962035697972",
            ),
            (
                re.compile(r"DS4424N\+T&R/KiCad/SON40P300X300X80-15N\.kicad_mod"),
                "68688c38fa5d92b6ba580cc1a017e18f706f6e7582f00ecb5a9e712010fbecac",
            ),
            (
                re.compile(r"DS4424N\+T&R/3D/DS4424N\+T&R\.stp"),
                "d19e992a8e045d6d67ee2e45fbd1bad91a7412a375390366f23da2a383bd8e72",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_MCP659-E_ML.zip"),
        [
            (
                re.compile(r"MCP659-E_ML/KiCad/MCP659-E_ML\.kicad_sym"),
                "aa230ca193e6803deac84522e3a15c536ecf7a2ca21e39807d062d3b9521faf9",
            ),
            (
                re.compile(r"MCP659-E_ML/KiCad/QFN65P400X400X100-17N-D\.kicad_mod"),
                "81e77a738eeb0811d3c2d9d616e84dccf4df7bb67520dc6ba07b24e73b2b914f",
            ),
            (
                re.compile(r"MCP659-E_ML/3D/MCP659-E_ML\.stp"),
                "a516db06f9c4ca513d6abbbabcf0a956fcda2bc4f86bdf3c9439f42b7e0ae690",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_SK6805-EC15.zip"),
        [
            (
                re.compile(r"SK6805-EC15/KiCad/SK6805-EC15\.kicad_sym"),
                "77a647ea858def8364ecba66956c6fdfdea4c09e2c0a8b94295358ea37012d63",
            ),
            (
                re.compile(r"SK6805-EC15/KiCad/SK6805EC15\.kicad_mod"),
                "e1dc39cad2d3fc322f337a5b51e06bf3a04d6661c17bce43ec8a3d7bb97b9a76",
            ),
            (
                re.compile(r"SK6805-EC15/3D/SK6805-EC15\.stp"),
                "2d9447015b4800b7e6d31c0da52cc7fa227693080d0a520d3b8b8b334dda8fbe",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_TC42X-2-102E.zip"),
        [
            (
                re.compile(r"TC42X-2-102E/KiCad/TC42X-2-102E\.kicad_sym"),
                "a7188a947a8c9fe469d2ffe386a6f8f1a39b33075c490c30d8b27c22e2a7595f",
            ),
            (
                re.compile(r"TC42X-2-102E/KiCad/TC42X2102E\.kicad_mod"),
                "21185e9748388b345805631fcf86d35e53f921551985abb07d7bbdc0fbdc4c00",
            ),
            (
                re.compile(r"TC42X-2-102E/3D/TC42X-2-102E\.stp"),
                "5209c21684bdeb9b537a96e50d5d875babf3b80a4f1ba964d5a2ff38f2c99c45",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_W25Q16JVUXIQ.zip"),
        [
            (
                re.compile(r"W25Q16JVUXIQ/KiCad/W25Q16JVUXIQ\.kicad_sym"),
                "3950a6bec2de7ab394b59addb3d076008a89d1b137f669c085cf62e7eecf72c2",
            ),
            (
                re.compile(r"W25Q16JVUXIQ/KiCad/SON50P300X200X60-9N\.kicad_mod"),
                "a87214a32557c5b76aacfd60dde051d595ee152e77fdfd79e3a4b3f9440d254e",
            ),
            (
                re.compile(r"W25Q16JVUXIQ/3D/W25Q16JVUXIQ\.stp"),
                "05ad1ea726e5177f628cce20d117f2648a2c35c9b77ad6be5ad27cd83d2789c4",
            ),
        ],
    ),
    (
        pathlib.Path("3rd_party/LIB_XCL103D503CR-G.zip"),
        [
            (
                re.compile(r"XCL103D503CR-G/KiCad/XCL103D503CR-G\.kicad_sym"),
                "9d3dfa841914e52778b306a917204f59bacdbbc0bfae043327e6cd87df23d04b",
            ),
            (
                re.compile(r"XCL103D503CR-G/KiCad/XCL103D503CRG\.kicad_mod"),
                "eb6c7ec76f48ac3cb36a9136e6b3f21294fead8d84e3effd8bdfe804bf002324",
            ),
            (
                re.compile(r"XCL103D503CR-G/3D/XCL103D503CR-G\.stp"),
                "e041e96ec9c52ece6b0aa7423609c03bcab3e2a2fb0074bfdf1ef669c9d82e1d",
            ),
        ],
    ),
]

for library in libraries:
    _verify_library(library)
    print(library[0])

    target_dir = library[0].parent / library[0].stem
    if target_dir.exists():
        shutil.rmtree(target_dir, ignore_errors=True)
    os.makedirs(target_dir, exist_ok=True)

    with zipfile.ZipFile(library[0], "r") as zip_ref:
        zip_ref.extractall(target_dir)

# The filename of the kicad_sym downloaded from Ultra Librarian is the datetime of the download and changes every time.
for path in [
    pathlib.Path(filename)
    for filename in glob.glob("3rd_party/ul_*/KiCADv6/*.kicad_sym")
]:
    match = re.search(r"ul_(.+?)/", str(path.as_posix()))
    assert match is not None

    new_filename = match.group(1) + ".kicad_sym"
    shutil.move(path, path.parent / new_filename)
