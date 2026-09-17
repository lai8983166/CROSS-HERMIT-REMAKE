
undefined4 FUN__text__00582980(short param_1)

{
  uint local_c;
  
  local_c = 0;
  while( true ) {
    if (9 < local_c) {
      return 1;
    }
    if (param_1 == *(short *)(&DAT_00764bc4 + local_c * 2)) break;
    local_c = local_c + 1;
  }
  return 0;
}

