
void FUN__text__00479820(int param_1)

{
  short sVar1;
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
  local_14 = &DAT_006149d0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 10;
  local_18 = *local_10;
  if (local_18 == '\0') {
    FUN__text__0046b0b0(param_1,1);
    FUN__text__0046b0f0(param_1,1);
    *local_10 = *local_10 + '\x01';
    FUN__text__0046bcc0(param_1,(int)(char)local_14[1]);
    FUN__text__0046be50(param_1,(int)*(short *)(local_14 + 6),0,0);
    FUN__text__0049ad90(param_1,0x70);
    *(undefined4 *)(*(int *)(param_1 + 600) + 0x24) = 0;
  }
  else if (local_18 == '\x01') {
    if (*(char *)(param_1 + 4) != '\0') {
      *local_10 = *local_10 + '\x01';
      *(undefined2 *)(param_1 + 10) = 0;
    }
  }
  else if ((local_18 == '\x02') &&
          (sVar1 = *(short *)(param_1 + 10), iVar2 = FUN__text__00415070(0x46), iVar2 < sVar1)) {
    FUN__text__0046b0b0(param_1,0);
    FUN__text__0046b0f0(param_1,0);
    FUN__text__00475370(param_1,0xb,0xffffffff);
    FUN__text__0046ba10(param_1);
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xf) = 4;
    FUN__text__00430b20(param_1);
  }
  local_8 = 0x4799ac;
  FUN__text__0056ce80();
  return;
}

