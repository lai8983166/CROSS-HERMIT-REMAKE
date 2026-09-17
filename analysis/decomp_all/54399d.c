
void FUN__text__0054399d(undefined4 *param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  char *pcVar5;
  undefined4 local_44 [16];
  
  puVar3 = param_1;
  puVar4 = local_44;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  puVar3 = param_1;
  for (iVar2 = 0x67; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  }
  puVar3 = local_44;
  puVar4 = param_1;
  for (iVar2 = 0x10; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  param_1[0x28] = 0x2000;
  uVar1 = FUN__text__0054bc20(param_1,0x2000);
  param_1[0x27] = uVar1;
  param_1[0x21] = FUN__text__00546672;
  param_1[0x22] = thunk_FUN__text__0054bc56;
  param_1[0x23] = param_1;
  iVar2 = FUN__text__0054b70a(param_1 + 0x19,"1.1.3",0x38);
  if (iVar2 == -6) {
    pcVar5 = "zlib version";
  }
  else if ((iVar2 == -4) || (iVar2 == -2)) {
    pcVar5 = "zlib memory";
  }
  else {
    if (iVar2 == 0) goto LAB__text__00543a39;
    pcVar5 = "Unknown zlib error";
  }
  FUN__text__0054381d(param_1,pcVar5);
LAB__text__00543a39:
  param_1[0x1c] = param_1[0x27];
  param_1[0x1d] = param_1[0x28];
  FUN__text__005465a0(param_1,0,0);
  return;
}

