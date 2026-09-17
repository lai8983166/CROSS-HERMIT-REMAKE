
void FUN__text__00544170(undefined4 *param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 *puVar5;
  int iVar6;
  undefined4 *puVar7;
  undefined4 local_44 [16];
  
  iVar6 = 0;
  if (param_2 != 0) {
    FUN__text__0054672f(param_1,param_2);
  }
  if (param_3 != 0) {
    FUN__text__0054672f(param_1,param_3);
  }
  FUN__text__0054bc56(param_1,param_1[0x27]);
  FUN__text__0054bc56(param_1,param_1[0x37]);
  FUN__text__0054bc56(param_1,param_1[0x36]);
  FUN__text__0054bc56(param_1,param_1[0x5d]);
  FUN__text__0054bc56(param_1,param_1[0x5e]);
  FUN__text__0054bc56(param_1,param_1[0x4e]);
  if ((*(byte *)((int)param_1 + 0x5d) & 0x10) != 0) {
    thunk_FUN__text__0054bc56(param_1,param_1[0x41]);
  }
  if ((*(byte *)((int)param_1 + 0x5d) & 0x20) != 0) {
    FUN__text__0054bc56(param_1,param_1[0x57]);
  }
  if (param_1[0x51] != 0) {
    iVar4 = 1 << (8U - (char)param_1[0x4b] & 0x1f);
    if (0 < iVar4) {
      do {
        FUN__text__0054bc56(param_1,*(undefined4 *)(param_1[0x51] + iVar6 * 4));
        iVar6 = iVar6 + 1;
      } while (iVar6 < iVar4);
    }
    FUN__text__0054bc56(param_1,param_1[0x51]);
  }
  FUN__text__0054b5e7(param_1 + 0x19);
  uVar1 = param_1[0x12];
  uVar2 = param_1[0x10];
  puVar5 = param_1;
  puVar7 = local_44;
  for (iVar6 = 0x10; iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar7 = *puVar5;
    puVar5 = puVar5 + 1;
    puVar7 = puVar7 + 1;
  }
  uVar3 = param_1[0x11];
  puVar5 = param_1;
  for (iVar6 = 0x67; iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar5 = 0;
    puVar5 = puVar5 + 1;
  }
  param_1[0x11] = uVar3;
  puVar5 = local_44;
  puVar7 = param_1;
  for (iVar6 = 0x10; iVar6 != 0; iVar6 = iVar6 + -1) {
    *puVar7 = *puVar5;
    puVar5 = puVar5 + 1;
    puVar7 = puVar7 + 1;
  }
  param_1[0x10] = uVar2;
  param_1[0x12] = uVar1;
  return;
}

