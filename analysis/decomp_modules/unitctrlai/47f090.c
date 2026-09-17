
void FUN__text__0047f090(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  char local_20;
  int local_1c;
  int local_18;
  char *local_14;
  undefined1 *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (undefined1 *)FUN__text__0047a8e0(param_1);
  local_14 = (char *)FUN__text__0047a800(param_1);
  local_1c = (int)*local_14;
  local_18 = *(int *)(local_14 + 4);
  local_20 = *(char *)(local_18 + 8 + *(char *)(local_c + 0x19) * 0xc);
  if (local_20 == '\0') {
    *(char *)(local_c + 0x19) = *(char *)(local_c + 0x19) + '\x01';
    if (local_1c <= *(char *)(local_c + 0x19)) {
      *(undefined1 *)(local_c + 0x19) = 0;
    }
  }
  else {
    if (local_20 == -1) {
      *local_10 = 0;
      goto LAB__text__0047f1b0;
    }
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xa2) =
         *(undefined1 *)(local_18 + 8 + *(char *)(local_c + 0x19) * 0xc);
    *(undefined1 *)(local_c + 0x19) = 0;
    local_14 = (char *)FUN__text__0047a800(param_1);
    local_18 = *(int *)(local_14 + 4);
  }
  FUN__text__0047d190(param_1,*(undefined1 *)(local_18 + *(char *)(local_c + 0x19) * 0xc),
                      *(undefined1 *)(local_18 + 1 + *(char *)(local_c + 0x19) * 0xc));
LAB__text__0047f1b0:
  local_8 = 0x47f1bd;
  FUN__text__0056ce80();
  return;
}

