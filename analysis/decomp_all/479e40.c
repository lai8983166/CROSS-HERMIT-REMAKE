
void FUN__text__00479e40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  char local_18;
  undefined *local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  iVar2 = FUN__text__00468d80(param_1);
  if ((iVar2 != 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059d3f0,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e20 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = &DAT_006149d0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 10;
  local_18 = *local_10;
  if (local_18 == '\0') {
    FUN__text__0046b0b0(param_1,0);
    FUN__text__0046b0f0(param_1,0);
    FUN__text__00475370(param_1,0xb,0xffffffff);
    FUN__text__0046ba10(param_1);
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 0;
  }
  local_8 = 0x479f34;
  FUN__text__0056ce80();
  return;
}

