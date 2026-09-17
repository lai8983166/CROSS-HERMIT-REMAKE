
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00497980(undefined4 param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  float local_8;
  
  puVar4 = local_48;
  for (iVar3 = 0x11; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (DAT_007a49f8 == 0) {
    iVar3 = FUN__text__00424f80("ScriptWork!=0",
                                "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlScript.CPP",
                                DAT_00619fc0 + 2,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined4 *)(DAT_007a49f8 + 0x2490) = 0x9800;
  *(undefined1 *)(DAT_007a49f8 + 0x2498) = 0;
  *(undefined1 *)(DAT_007a49f8 + 0x249a) = 1;
  *(undefined4 *)(DAT_007a49f8 + 0x249c) = param_1;
  *(undefined1 *)(DAT_007a49f8 + 0x2499) = 1;
  local_8 = _DAT_0059e8bc / (float)*(int *)(DAT_007a49f8 + 0x249c);
  uVar2 = __ftol();
  *(undefined4 *)(DAT_007a49f8 + 0x2494) = uVar2;
  local_8 = 6.74784e-39;
  FUN__text__0056ce80();
  return;
}

