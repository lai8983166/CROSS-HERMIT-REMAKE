
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* Library Function - Single Match
    __XcptFilter
   
   Library: Visual Studio 2003 Debug */

int __cdecl __XcptFilter(ulong _ExceptionNum,_EXCEPTION_POINTERS *_ExceptionPtr)

{
  code *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  int *piVar5;
  int local_18;
  
  iVar4 = FUN__text__005753b0();
  piVar5 = (int *)FUN__text__00576f00(_ExceptionNum,*(undefined4 *)(iVar4 + 0x50));
  if ((piVar5 == (int *)0x0) || (piVar5[2] == 0)) {
    iVar4 = (*API_KERNEL32_DLL_UnhandledExceptionFilter)(_ExceptionPtr);
  }
  else if (piVar5[2] == 5) {
    piVar5[2] = 0;
    iVar4 = 1;
  }
  else if (piVar5[2] == 1) {
    iVar4 = -1;
  }
  else {
    pcVar1 = (code *)piVar5[2];
    uVar2 = *(undefined4 *)(iVar4 + 0x54);
    *(_EXCEPTION_POINTERS **)(iVar4 + 0x54) = _ExceptionPtr;
    if (piVar5[1] == 8) {
      for (local_18 = DAT_00761de0; local_18 < DAT_00761de0 + _DAT_00761de4; local_18 = local_18 + 1
          ) {
        *(undefined4 *)(*(int *)(iVar4 + 0x50) + 8 + local_18 * 0xc) = 0;
      }
      uVar3 = *(undefined4 *)(iVar4 + 0x58);
      if (*piVar5 == -0x3fffff72) {
        *(undefined4 *)(iVar4 + 0x58) = 0x83;
      }
      else if (*piVar5 == -0x3fffff70) {
        *(undefined4 *)(iVar4 + 0x58) = 0x81;
      }
      else if (*piVar5 == -0x3fffff6f) {
        *(undefined4 *)(iVar4 + 0x58) = 0x84;
      }
      else if (*piVar5 == -0x3fffff6d) {
        *(undefined4 *)(iVar4 + 0x58) = 0x85;
      }
      else if (*piVar5 == -0x3fffff73) {
        *(undefined4 *)(iVar4 + 0x58) = 0x82;
      }
      else if (*piVar5 == -0x3fffff71) {
        *(undefined4 *)(iVar4 + 0x58) = 0x86;
      }
      else if (*piVar5 == -0x3fffff6e) {
        *(undefined4 *)(iVar4 + 0x58) = 0x8a;
      }
      (*pcVar1)(8,*(undefined4 *)(iVar4 + 0x58));
      *(undefined4 *)(iVar4 + 0x58) = uVar3;
    }
    else {
      piVar5[2] = 0;
      (*pcVar1)(piVar5[1]);
    }
    *(undefined4 *)(iVar4 + 0x54) = uVar2;
    iVar4 = -1;
  }
  return iVar4;
}

