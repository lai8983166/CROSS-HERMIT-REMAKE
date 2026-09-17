
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0041e7f0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  iVar2 = FUN__text__0041d790();
  if (((iVar2 != 0) && (*(char *)(local_8 + 0x22) != '\0')) && (*(int *)(local_8 + 0x260) != 0)) {
    *(int *)(local_8 + 0x270) = *(int *)(local_8 + 0x270) + 1;
    if (*(int *)(local_8 + 0x260) <= *(int *)(local_8 + 0x270)) {
      local_c = 1;
    }
    *(float *)(local_8 + 0x26c) = *(float *)(local_8 + 0x26c) - *(float *)(local_8 + 0x268);
    if (*(float *)(local_8 + 0x26c) < _DAT_005946ac) {
      *(undefined4 *)(local_8 + 0x26c) = 0xc59c4000;
    }
    *(int *)(local_8 + 0x274) = *(int *)(local_8 + 0x274) + 1;
    if (*(int *)(local_8 + 0x274) < 4) {
      uVar1 = __ftol();
      FUN__text__0041da80(uVar1);
      *(undefined4 *)(local_8 + 0x274) = 0;
    }
    if (local_c != 0) {
      FUN__text__0041e6b0();
      FUN__text__0041e500();
    }
  }
  local_8 = 0x41e934;
  FUN__text__0056ce80();
  return;
}

