
void FUN__text__00476470(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  char local_1c;
  uint local_18;
  uint local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)FUN__text__0047a8e0(param_1);
  *(undefined1 *)(param_1 + 0x2a7) = 1;
  iVar2 = FUN__text__00468d80(param_1);
  if (((iVar2 == 0) && (*(char *)(*(int *)(param_1 + 600) + 0xa0) == '\0')) && (*local_10 == '\x01')
     ) {
LAB__text__004765ae:
    if (*(char *)(*(int *)(param_1 + 600) + 0x30) != '\x04') {
      FUN__text__00475270(param_1,0x10);
      goto switchD__text__00476589_default;
    }
    goto switchD__text__00476503_caseD_2;
  }
  local_14 = (uint)*(byte *)(*(int *)(param_1 + 600) + 0x9f);
  switch(local_14) {
  case 0:
    cVar1 = *(char *)(*(int *)(param_1 + 600) + 0x30);
    break;
  case 1:
    cVar1 = *(char *)(*(int *)(param_1 + 600) + 0x30);
    break;
  case 2:
    goto switchD__text__00476503_caseD_2;
  case 3:
    FUN__text__00475270(param_1,2);
    goto switchD__text__00476589_default;
  default:
    goto switchD__text__00476503_default;
  }
  if (cVar1 == '\x04') goto switchD__text__00476503_caseD_2;
switchD__text__00476503_default:
  local_18 = (uint)*(byte *)(*(int *)(param_1 + 600) + 0xa0);
  switch(local_18) {
  case 0:
    local_1c = *local_10;
    if (local_1c != '\0') {
      if (local_1c == '\x01') goto LAB__text__004765ae;
      if (local_1c != '\x02') goto switchD__text__00476589_default;
      if (*(char *)(*(int *)(param_1 + 600) + 0x30) != '\x04') {
        FUN__text__00475270(param_1,0x17);
        goto switchD__text__00476589_default;
      }
    }
    break;
  case 1:
    break;
  case 2:
    break;
  case 3:
    break;
  case 4:
    FUN__text__00475270(param_1,0x16);
  default:
    goto switchD__text__00476589_default;
  }
switchD__text__00476503_caseD_2:
  FUN__text__00475270(param_1,0x13);
switchD__text__00476589_default:
  local_8 = 0x476647;
  FUN__text__0056ce80();
  return;
}

