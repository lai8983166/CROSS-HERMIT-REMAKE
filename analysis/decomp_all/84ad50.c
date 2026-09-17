
void FUN__text1__0084ad50(DWORD param_1)

{
  DWORD *pDVar1;
  DWORD DVar2;
  size_t sVar3;
  HANDLE hFile;
  int iVar4;
  char acStackY_1e3 [7];
  undefined1 *puStackY_1dc;
  char *pcStackY_1d8;
  undefined4 uStackY_1d4;
  undefined1 *puStackY_1d0;
  undefined4 uStackY_1cc;
  undefined1 *puStackY_1c8;
  undefined *puStackY_1c4;
  LPCVOID lpBuffer;
  LPDWORD lpNumberOfBytesWritten;
  LPOVERLAPPED lpOverlapped;
  CHAR local_1a8 [260];
  undefined1 local_a4 [160];
  
  iVar4 = 0;
  pDVar1 = &DAT_00870518;
  do {
    if (param_1 == *pDVar1) break;
    pDVar1 = pDVar1 + 2;
    iVar4 = iVar4 + 1;
  } while ((int)pDVar1 < 0x8705a8);
  if (param_1 == (&DAT_00870518)[iVar4 * 2]) {
    if ((DAT_008756c0 == 1) || ((DAT_008756c0 == 0 && (DAT_00870254 == 1)))) {
      lpNumberOfBytesWritten = &param_1;
      lpOverlapped = (LPOVERLAPPED)0x0;
      sVar3 = _strlen(*(char **)(&UNK_0087051c + iVar4 * 8));
      lpBuffer = *(LPCVOID *)(&UNK_0087051c + iVar4 * 8);
      puStackY_1c4 = (undefined *)0x84ae99;
      hFile = GetStdHandle(0xfffffff4);
      puStackY_1c4 = (undefined *)0x84aea0;
      WriteFile(hFile,lpBuffer,sVar3,lpNumberOfBytesWritten,lpOverlapped);
    }
    else if (param_1 != 0xfc) {
      DVar2 = GetModuleFileNameA((HMODULE)0x0,local_1a8,0x104);
      if (DVar2 == 0) {
        FUN__text1__00848d20();
      }
      sVar3 = _strlen(local_1a8);
      if (0x3c < sVar3 + 1) {
        sVar3 = _strlen(local_1a8);
        puStackY_1c4 = (undefined *)0x84ae1a;
        _strncpy(acStackY_1e3 + sVar3,"...",3);
      }
      FUN__text1__00848d20();
      puStackY_1c4 = (undefined *)0x84ae3b;
      FUN__text1__00848d30();
      puStackY_1c8 = local_a4;
      puStackY_1c4 = &DAT_008742ec;
      uStackY_1cc = 0x84ae4c;
      FUN__text1__00848d30();
      uStackY_1cc = *(undefined4 *)(&UNK_0087051c + iVar4 * 8);
      puStackY_1d0 = local_a4;
      uStackY_1d4 = 0x84ae5e;
      FUN__text1__00848d30();
      uStackY_1d4 = 0x12010;
      puStackY_1dc = local_a4;
      pcStackY_1d8 = "Microsoft Visual C++ Runtime Library";
      acStackY_1e3[3] = 't';
      acStackY_1e3[4] = -0x52;
      acStackY_1e3[5] = -0x7c;
      acStackY_1e3[6] = '\0';
      FUN__text1__0084d318();
    }
  }
  return;
}

