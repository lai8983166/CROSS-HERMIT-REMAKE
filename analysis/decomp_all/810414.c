
int FUN__text1__00810414(undefined4 param_1,undefined1 *param_2)

{
  undefined1 local_244c;
  undefined1 *local_2448;
  undefined1 local_2444 [9268];
  undefined4 uStack_10;
  undefined1 *puStack_c;
  undefined1 *local_8;
  
  local_8 = (undefined1 *)0x810421;
  FUN__text1__00848c20();
  local_2448 = param_2;
  local_8 = local_2444;
  puStack_c = (undefined1 *)0x810442;
  FUN__text1__0080fc08();
  while (local_2448 < local_8) {
    local_8 = (undefined1 *)param_1;
    puStack_c = local_2444;
    uStack_10 = 0x810460;
    local_8 = (undefined1 *)FUN__text1__008104b9();
    if (local_8 == (undefined1 *)0x100) break;
    local_244c = SUB41(local_8,0);
    *local_2448 = local_244c;
    local_2448 = local_2448 + 1;
    puStack_c = local_2444;
    uStack_10 = 0x8104a7;
    FUN__text1__0080fdb3();
  }
  return (int)local_2448 - (int)param_2;
}

